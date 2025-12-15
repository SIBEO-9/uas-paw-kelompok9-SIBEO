"""
Views dengan decorator yang konsisten - FIX for error 500
"""
from pyramid.view import view_config
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

# ⭐⭐ HANYA IMPORT DARI DECORATORS - JANGAN BUAT LAGI! ⭐⭐
from .decorators import login_required, instructor_only, student_only, owner_required

# Import response helpers
from .response_helpers import (
    success_response, created_response, no_content_response,
    bad_request_error, unauthorized_error, forbidden_error,
    not_found_error, conflict_error, server_error,
    validate_required_fields
)

from .models import DBSession, User, Course, Module, Enrollment

# Helper function untuk mendapatkan current user
def get_current_user(request):
    """Helper untuk mendapatkan user object dari session dengan type safety"""
    user_id_str = request.session.get('user_id')
    if not user_id_str:
        return None
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        return None
    
    dbsession = DBSession()
    return dbsession.query(User).filter_by(id=user_id).first()

# Helper untuk cek apakah user terenroll di course
def is_enrolled_in_course(student_id, course_id):
    """Cek apakah student sudah terdaftar di course"""
    dbsession = DBSession()
    enrollment = dbsession.query(Enrollment).filter_by(
        student_id=student_id, 
        course_id=course_id
    ).first()
    return enrollment is not None

# --- HOME VIEW ---
@view_config(route_name='home', renderer='json')
def home_view(request):
    return success_response(
        message='Welcome to LMS API Platform',
        data={
            'endpoints': {
                'register': '/api/register',
                'login': '/api/login',
                'users': '/api/users',
                'courses': '/api/courses',
                'enrollments': '/api/enrollments',
                'modules': '/api/courses/{id}/modules'
            }
        }
    )

# --- AUTHENTICATION VIEWS ---
@view_config(route_name='register', renderer='json')
def register(request):
    """Register new user with password hashing"""
    dbsession = DBSession()
    try:
        try:
            data = request.json_body
        except ValueError:
            return bad_request_error('Invalid JSON format')
        
        required_fields = ['name', 'email', 'password', 'role']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error
        
        if data['role'] not in ['student', 'instructor']:
            return bad_request_error("Role must be 'student' or 'instructor'")
        
        existing_user = dbsession.query(User).filter(User.email == data['email']).first()
        if existing_user:
            return conflict_error('Email already registered')
        
        new_user = User.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data['role']
        )
        
        dbsession.add(new_user)
        dbsession.flush()
        
        # Start session for new user
        request.session['user_id'] = new_user.id
        request.session['user_email'] = new_user.email
        request.session['user_role'] = new_user.role
        
        return created_response(
            data=new_user.to_dict(),
            message='Registration successful'
        )
        
    except IntegrityError:
        dbsession.rollback()
        return conflict_error('Email already exists')
    except Exception as e:
        dbsession.rollback()
        print(f"🔥 ERROR in register: {str(e)}")
        return server_error(f'Registration failed: {str(e)}')

@view_config(route_name='login', renderer='json')
def login(request):
    """Login user and create session"""
    dbsession = DBSession()
    try:
        try:
            data = request.json_body
        except ValueError:
            return bad_request_error('Invalid JSON format')
        
        if 'email' not in data or 'password' not in data:
            return bad_request_error('Email and password required')
        
        user = dbsession.query(User).filter(User.email == data['email']).first()
        
        if not user:
            return unauthorized_error('Invalid email or password')
        
        if not user.verify_password(data['password']):
            return unauthorized_error('Invalid email or password')
        
        # Create session
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['user_role'] = user.role
        
        return success_response(
            data=user.to_dict(),
            message='Login successful'
        )
        
    except Exception as e:
        print(f"🔥 ERROR in login: {str(e)}")
        return server_error(f'Login failed: {str(e)}')

@view_config(route_name='logout', renderer='json')
def logout(request):
    """Logout user by clearing session"""
    request.session.invalidate()
    return success_response(message='Logout successful')

# --- USER VIEWS ---
@view_config(route_name='users', renderer='json')
def get_all_users(request):
    try:
        dbsession = DBSession()
        users = dbsession.query(User).all()
        return success_response(
            data=[u.to_dict() for u in users],
            count=len(users)
        )
    except Exception as e:
        return server_error('Failed to retrieve users')

@view_config(route_name='create_user', renderer='json')
def create_user(request):
    try:
        dbsession = DBSession()
        data = request.json_body
        
        required_fields = ['name', 'email', 'password', 'role']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error
        
        new_user = User.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data['role']
        )
        
        dbsession.add(new_user)
        dbsession.flush()
        
        return created_response(
            data=new_user.to_dict(),
            message='User created successfully'
        )
        
    except IntegrityError:
        dbsession.rollback()
        return conflict_error('Email already exists')
    except Exception as e:
        return server_error(f'Failed to create user: {str(e)}')

@view_config(route_name='user_detail', renderer='json')
def get_user_detail(request):
    try:
        dbsession = DBSession()
        user_id = int(request.matchdict.get('id'))
        user = dbsession.query(User).filter(User.id == user_id).first()
        if not user:
            return not_found_error('User not found')
        
        return success_response(data=user.to_dict())
        
    except ValueError:
        return bad_request_error('Invalid user ID')
    except Exception as e:
        return server_error('Failed to retrieve user details')

# --- COURSE VIEWS ---
@view_config(route_name='get_all_courses', renderer='json')
def get_all_courses(request):
    try:
        dbsession = DBSession()
        courses = dbsession.query(Course).all()
        return success_response(
            data=[c.to_dict() for c in courses],
            count=len(courses)
        )
    except Exception as e:
        return server_error('Failed to retrieve courses')

@view_config(route_name='get_course_detail', renderer='json')
def get_course_detail(request):
    try:
        dbsession = DBSession()
        course_id = int(request.matchdict.get('id'))
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        if not course:
            return not_found_error('Course not found')
        
        modules_count = dbsession.query(Module).filter(
            Module.course_id == course_id
        ).count()
        
        enrollments_count = dbsession.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).count()
        
        course_data = course.to_dict()
        course_data['modules_count'] = modules_count
        course_data['enrollments_count'] = enrollments_count
        
        return success_response(data=course_data)
        
    except ValueError:
        return bad_request_error('Invalid course ID')
    except Exception as e:
        return server_error('Failed to retrieve course details')

@view_config(route_name='create_course', renderer='json')
@login_required
@instructor_only
def create_course(request):
    try:
        print("DEBUG: Entering create_course method")
        
        current_user = get_current_user(request)
        print(f"DEBUG: Current user: {current_user.id if current_user else 'None'}")
        
        if not current_user:
            return unauthorized_error('User not found')
        
        data = request.json_body
        print(f"DEBUG: Request data: {data}")
        
        required_fields = ['title', 'description']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            print(f"DEBUG: Validation failed")
            return validation_error
        
        print(f"DEBUG: Creating course...")
        dbsession = DBSession()
        new_course = Course(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            instructor_id=current_user.id
        )
        
        dbsession.add(new_course)
        dbsession.flush()
        
        print(f"DEBUG: Course created with ID: {new_course.id}")
        
        return created_response(
            data=new_course.to_dict(),
            message='Course created successfully'
        )
        
    except Exception as e:
        print(f"🔥 ERROR in create_course: {str(e)}")
        import traceback
        traceback.print_exc()
        return server_error(f'Failed to create course: {str(e)}')

@view_config(route_name='update_course', renderer='json')
@login_required
@owner_required(Course, id_param='id', owner_field='instructor_id')
def update_course(request):
    try:
        dbsession = DBSession()
        course_id = int(request.matchdict.get('id'))
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            return not_found_error('Course not found')
        
        data = request.json_body
        
        if 'title' in data:
            course.title = data['title']
        if 'description' in data:
            course.description = data['description']
        if 'category' in data:
            course.category = data['category']
        
        dbsession.flush()
        
        return success_response(
            data=course.to_dict(),
            message='Course updated successfully'
        )
        
    except ValueError:
        return bad_request_error('Invalid course ID')
    except Exception as e:
        return server_error(f'Failed to update course: {str(e)}')

@view_config(route_name='delete_course', renderer='json')
@login_required
@owner_required(Course, id_param='id', owner_field='instructor_id')
def delete_course(request):
    try:
        dbsession = DBSession()
        course_id = int(request.matchdict.get('id'))
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            return not_found_error('Course not found')
        
        course_title = course.title
        dbsession.delete(course)
        dbsession.flush()
        
        return no_content_response(f'Course "{course_title}" deleted successfully')
        
    except ValueError:
        return bad_request_error('Invalid course ID')
    except Exception as e:
        return server_error(f'Failed to delete course: {str(e)}')

# --- ENROLLMENT VIEWS ---
@view_config(route_name='create_enrollment', renderer='json')
@login_required
@student_only
def create_enrollment(request):
    try:
        current_user = get_current_user(request)
        if not current_user:
            return unauthorized_error('User not found')
        
        dbsession = DBSession()
        data = request.json_body
        
        if 'course_id' not in data:
            return bad_request_error('course_id is required')
        
        try:
            course_id = int(data['course_id'])
        except ValueError:
            return bad_request_error('Invalid course ID')
        
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        if not course:
            return not_found_error('Course not found')
        
        existing_enrollment = dbsession.query(Enrollment).filter_by(
            student_id=current_user.id,
            course_id=course_id
        ).first()
        
        if existing_enrollment:
            return conflict_error('Already enrolled in this course')
        
        enrollment = Enrollment(
            student_id=current_user.id,
            course_id=course_id
        )
        
        dbsession.add(enrollment)
        dbsession.flush()
        
        return created_response(
            data=enrollment.to_dict(),
            message='Enrolled successfully'
        )
        
    except Exception as e:
        return server_error(f'Failed to enroll: {str(e)}')

@view_config(route_name='get_my_enrollments', renderer='json')
@login_required
@student_only
def get_my_enrollments(request):
    try:
        current_user = get_current_user(request)
        if not current_user:
            return unauthorized_error('User not found')
        
        dbsession = DBSession()
        enrollments = dbsession.query(Enrollment).filter_by(
            student_id=current_user.id
        ).all()
        
        enrollment_data = []
        for enroll in enrollments:
            course = dbsession.query(Course).filter_by(id=enroll.course_id).first()
            if course:
                enrollment_data.append({
                    'enrollment_id': enroll.id,
                    'enrolled_date': enroll.enrolled_date.isoformat() if enroll.enrolled_date else None,
                    'course': course.to_dict()
                })
        
        return success_response(
            data=enrollment_data,
            count=len(enrollment_data)
        )
        
    except Exception as e:
        return server_error('Failed to retrieve enrollments')

@view_config(route_name='delete_enrollment', renderer='json')
@login_required
@student_only
def delete_enrollment(request):
    try:
        current_user = get_current_user(request)
        if not current_user:
            return unauthorized_error('User not found')
        
        dbsession = DBSession()
        enrollment_id = int(request.matchdict.get('id'))
        
        enrollment = dbsession.query(Enrollment).filter_by(id=enrollment_id).first()
        if not enrollment:
            return not_found_error('Enrollment not found')
        
        if enrollment.student_id != current_user.id:
            return forbidden_error('Access denied. This is not your enrollment')
        
        course = dbsession.query(Course).filter_by(id=enrollment.course_id).first()
        course_title = course.title if course else f"Course {enrollment.course_id}"
        
        dbsession.delete(enrollment)
        dbsession.flush()
        
        return no_content_response(f'Unenrolled from "{course_title}" successfully')
        
    except ValueError:
        return bad_request_error('Invalid enrollment ID')
    except Exception as e:
        return server_error(f'Failed to unenroll: {str(e)}')

# --- MODULE VIEWS ---
@view_config(route_name='get_course_modules', renderer='json')
@login_required
def get_course_modules(request):
    try:
        current_user = get_current_user(request)
        if not current_user:
            return unauthorized_error('User not found')
        
        dbsession = DBSession()
        course_id = int(request.matchdict.get('id'))
        
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        if not course:
            return not_found_error('Course not found')
        
        user_has_access = False
        
        if current_user.role == 'instructor':
            if course.instructor_id == current_user.id:
                user_has_access = True
        elif current_user.role == 'student':
            if is_enrolled_in_course(current_user.id, course_id):
                user_has_access = True
        
        if not user_has_access:
            return forbidden_error('Access denied. You must be enrolled in this course')
        
        modules = dbsession.query(Module).filter(
            Module.course_id == course_id
        ).order_by(Module.order).all()
        
        return success_response(
            data=[m.to_dict() for m in modules],
            count=len(modules),
            course_id=course_id,
            course_title=course.title
        )
        
    except ValueError:
        return bad_request_error('Invalid course ID')
    except Exception as e:
        return server_error('Failed to retrieve modules')

@view_config(route_name='create_course_module', renderer='json')
@login_required
@owner_required(Course, id_param='id', owner_field='instructor_id')
def create_course_module(request):
    try:
        dbsession = DBSession()
        course_id = int(request.matchdict.get('id'))
        course = dbsession.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            return not_found_error('Course not found')
        
        data = request.json_body
        
        required_fields = ['title', 'content']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error
        
        max_order = dbsession.query(
            func.max(Module.order)
        ).filter(Module.course_id == course_id).scalar() or 0
        
        new_module = Module(
            course_id=course_id,
            title=data.get('title'),
            content=data.get('content'),
            order=data.get('order', max_order + 1)
        )
        
        dbsession.add(new_module)
        dbsession.flush()
        
        return created_response(
            data=new_module.to_dict(),
            message='Module created successfully'
        )
        
    except Exception as e:
        return server_error(f'Failed to create module: {str(e)}')

@view_config(route_name='update_module', renderer='json')
@login_required
def update_module(request):
    try:
        dbsession = DBSession()
        module_id = int(request.matchdict.get('id'))
        module = dbsession.query(Module).filter(Module.id == module_id).first()
        
        if not module:
            return not_found_error('Module not found')
        
        current_user = get_current_user(request)
        course = dbsession.query(Course).filter(Course.id == module.course_id).first()
        
        if not course or course.instructor_id != current_user.id:
            return forbidden_error('Access denied. You are not the course instructor')
        
        data = request.json_body
        
        if 'title' in data:
            module.title = data['title']
        if 'content' in data:
            module.content = data['content']
        if 'order' in data:
            try:
                module.order = int(data['order'])
            except ValueError:
                return bad_request_error('Invalid order format')
        
        dbsession.flush()
        
        return success_response(
            data=module.to_dict(),
            message='Module updated successfully'
        )
        
    except ValueError:
        return bad_request_error('Invalid module ID')
    except Exception as e:
        return server_error(f'Failed to update module: {str(e)}')

@view_config(route_name='delete_module', renderer='json')
@login_required
def delete_module(request):
    try:
        dbsession = DBSession()
        module_id = int(request.matchdict.get('id'))
        module = dbsession.query(Module).filter(Module.id == module_id).first()
        
        if not module:
            return not_found_error('Module not found')
        
        current_user = get_current_user(request)
        course = dbsession.query(Course).filter(Course.id == module.course_id).first()
        
        if not course or course.instructor_id != current_user.id:
            return forbidden_error('Access denied. You are not the course instructor')
        
        module_title = module.title
        dbsession.delete(module)
        dbsession.flush()
        
        return no_content_response(f'Module "{module_title}" deleted successfully')
        
    except ValueError:
        return bad_request_error('Invalid module ID')
    except Exception as e:
        return server_error(f'Failed to delete module: {str(e)}')