#!/usr/bin/env python
"""
Script untuk inisialisasi database.
Gunakan Alembic untuk migration, bukan script ini langsung.
"""
import os
import sys
import argparse
from pyramid.paster import get_appsettings, setup_logging
from alembic.config import Config
from alembic import command

# Tambah path ke parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_migrations(ini_path='config/development.ini'):
    """Run Alembic migrations."""
    print(f"🚀 Menjalankan migration dari {ini_path}")
    
    # Setup logging
    setup_logging(ini_path)
    
    # Get database URL from config
    settings = get_appsettings(ini_path)
    
    # Setup Alembic config
    alembic_cfg = Config("alembic.ini")
    
    # Override with config from INI file
    alembic_cfg.set_main_option("sqlalchemy.url", settings['sqlalchemy.url'])
    
    # Run migrations
    print("📋 Menjalankan upgrade ke head...")
    command.upgrade(alembic_cfg, "head")
    print("✅ Migration selesai!")


def create_initial_data():
    """Create initial data (optional)."""
    print("📝 Membuat data awal...")
    # TODO: Tambahkan seed data jika diperlukan
    print("✅ Data awal selesai dibuat")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database initialization script')
    parser.add_argument(
        '--config', 
        default='config/development.ini',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--seed',
        action='store_true',
        help='Seed database with initial data'
    )
    
    args = parser.parse_args()
    
    # Run migrations
    run_migrations(args.config)
    
    # Seed data if requested
    if args.seed:
        create_initial_data()