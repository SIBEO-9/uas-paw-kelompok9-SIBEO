from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    
    # Database configuration
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    config.include('pyramid_retry')
    
    # Set up CORS (for future API development)
    config.add_cors_preflight_handler()
    
    # --- ROUTES ---
    
    # 1. Route untuk Homepage
    config.add_route('home', '/', request_method='GET')

    # 2. Routes untuk Users
    config.add_route('users', '/api/users', request_method='GET')
    config.add_route('create_user', '/api/users', request_method='POST')
    config.add_route('user_detail', '/api/users/{id}', request_method='GET')

    # 3. Routes untuk Courses
    config.add_route('courses', '/api/courses', request_method='GET')
    config.add_route('create_course', '/api/courses', request_method='POST')
    config.add_route('course_detail', '/api/courses/{id}', request_method='GET')

    # 4. Routes untuk Modules
    config.add_route('modules', '/api/courses/{course_id}/modules', request_method='GET')
    config.add_route('create_module', '/api/courses/{course_id}/modules', request_method='POST')

    # 5. Routes untuk Enrollments
    config.add_route('enroll', '/api/enroll', request_method='POST')
    
    # Scan views
    config.scan('.views')
    
    return config.make_wsgi_app()


def includeme(config):
    """For testing purposes."""
    config.scan('.views')