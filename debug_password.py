#!/usr/bin/env python
"""
Debug script untuk password hashing issue
"""
from src.e_learning.models import DBSession, User, pwd_context, Base
from sqlalchemy import create_engine, inspect
import sys

print('=' * 60)
print('DEBUG PASSWORD HASHING ISSUE')
print('=' * 60)

# 1. Setup database
engine = create_engine('postgresql://postgres:USSRussian@localhost/e_learning_dev')
DBSession.configure(bind=engine)

# 2. Cek user John Student
user = DBSession.query(User).filter_by(email='john.student@itera.ac.id').first()
if not user:
    print('❌ User not found!')
    sys.exit(1)

print(f'✅ User found: {user.name} (id: {user.id})')
print(f'   Email: {user.email}')
print(f'   Role: {user.role}')
print(f'   Password column type: {type(user.password)}')
print(f'   Password value: "{user.password}"')
print(f'   Password length: {len(user.password)}')

# 3. Cek apakah password kolom ada di database schema
inspector = inspect(engine)
columns = inspector.get_columns('users')
print(f'\n📊 Database schema for users table:')
for col in columns:
    if col['name'] == 'password':
        print(f'   {col["name"]}: {col["type"]} (nullable: {col["nullable"]})')

# 4. Test semua kemungkinan password
print(f'\n🔐 Testing password verification:')
test_passwords = [
    'simple123',      # Password yang dicoba
    'Simple123',
    'simple',
    '123',
    'password123',    # Password umum
    ''
]

for pwd in test_passwords:
    try:
        if not user.password:  # Jika password NULL/empty
            print(f'   Password "{pwd}": ❌ NO PASSWORD STORED')
            continue
            
        result = pwd_context.verify(pwd, user.password)
        print(f'   Password "{pwd}": {"✅ MATCH" if result else "❌ NO MATCH"}')
    except Exception as e:
        print(f'   Password "{pwd}": ❌ ERROR: {e}')

# 5. Test create new hash
print(f'\n🧪 Testing new hash creation:')
try:
    test_hash = pwd_context.hash('simple123')
    print(f'   New hash for "simple123": {test_hash[:50]}...')
    print(f'   New hash length: {len(test_hash)}')
    
    # Verify new hash works
    verify_result = pwd_context.verify('simple123', test_hash)
    print(f'   New hash verification: {"✅ SUCCESS" if verify_result else "❌ FAILED"}')
except Exception as e:
    print(f'   ❌ Hash creation failed: {e}')

# 6. Check method calls
print(f'\n🔧 Checking User.create_user method:')
try:
    test_user = User.create_user('Test', 'test@test.com', 'testpass', 'student')
    print(f'   create_user() returns: {type(test_user)}')
    print(f'   Password after create_user: {test_user.password[:30] if test_user.password else "EMPTY"}...')
except Exception as e:
    print(f'   ❌ create_user() failed: {e}')

print('\n' + '=' * 60)