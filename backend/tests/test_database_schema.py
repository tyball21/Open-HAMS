"""
Database Schema Validation Tests

These tests validate that the database schema matches expectations
and can help diagnose database-related issues.

Originally created to debug 422 errors in animal creation.
"""

# Import conftest to set up Python path
import conftest

import asyncio
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text
from api.deps import get_db_session


async def check_animal_table_schema():
    """Verify the animal table has the expected schema."""
    async for session in get_db_session():
        # Check animal table schema (PostgreSQL syntax)
        result = await session.exec(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'animal' 
            ORDER BY ordinal_position;
        """))
        columns = result.fetchall()
        
        # Expected columns and their properties
        expected_columns = {
            'name': ('character varying', False),
            'species': ('character varying', False), 
            'image_filename': ('character varying', True),
            'max_daily_checkouts': ('integer', False),
            'max_daily_checkout_hours': ('integer', True),
            'rest_time': ('double precision', True),
            'description': ('character varying', True),
            'tier': ('integer', False),
            'daily_checkout_count': ('integer', False),
            'daily_checkout_duration': ('interval', False),
            'last_checkin_time': ('timestamp with time zone', True),
            'checked_in': ('boolean', False),
            'handling_enabled': ('boolean', False),
            'status': ('character varying', True),
            'zoo_id': ('integer', False),
            'id': ('integer', False),
            'created_at': ('timestamp with time zone', True),
            'updated_at': ('timestamp with time zone', True)
        }
        
        schema_valid = True
        for col in columns:
            col_name, data_type, is_nullable = col[0], col[1], col[2] == 'YES'
            if col_name in expected_columns:
                expected_type, expected_nullable = expected_columns[col_name]
                if data_type != expected_type or is_nullable != expected_nullable:
                    print(f"❌ Column {col_name}: expected ({expected_type}, nullable={expected_nullable}), "
                          f"got ({data_type}, nullable={is_nullable})")
                    schema_valid = False
            else:
                print(f"⚠️  Unexpected column: {col_name}")
        
        print(f"✅ Animal table schema validation: {'PASSED' if schema_valid else 'FAILED'}")
        break
        
    return schema_valid


async def check_required_data_exists():
    """Verify that required reference data exists (zoos, etc.)."""
    async for session in get_db_session():
        # Check zoo table has at least one zoo
        result = await session.exec(text("SELECT COUNT(*) FROM zoo;"))
        zoo_count = result.fetchone()[0]
        
        if zoo_count == 0:
            print("❌ No zoos found in database - animals cannot be created")
            return False
        
        # Show available zoos for debugging
        result = await session.exec(text("SELECT id, name FROM zoo;"))
        zoos = result.fetchall()
        print(f"✅ Found {zoo_count} zoo(s):")
        for zoo in zoos:
            print(f"   ID: {zoo[0]}, Name: {zoo[1]}")
        
        break
    
    return True


def print_database_info():
    """Print comprehensive database information for debugging."""
    print("=" * 50)
    print("DATABASE SCHEMA VALIDATION")
    print("=" * 50)
    
    schema_valid = asyncio.run(check_animal_table_schema())
    data_valid = asyncio.run(check_required_data_exists())
    
    print("=" * 50)
    print(f"Overall Status: {'✅ READY' if schema_valid and data_valid else '❌ ISSUES FOUND'}")
    print("=" * 50)
    
    return schema_valid and data_valid


if __name__ == "__main__":
    print_database_info() 