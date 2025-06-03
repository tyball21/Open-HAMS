"""
Animal Model Creation and Validation Tests

These tests verify that the Animal and AnimalIn models work correctly
and can be used to create animals in the database.

Originally created to debug the 422 error where Animal.model_validate()
was incorrectly being called on AnimalIn data.
"""

# Import conftest to set up Python path
import conftest

import asyncio
import pytest
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from api.deps import get_db_session
from models import AnimalIn, Animal


async def test_animal_in_creation():
    """Test that AnimalIn objects can be created with valid data."""
    animal_data = AnimalIn(
        name="Test Lion",
        species="Panthera leo",
        max_daily_checkouts=1,
        max_daily_checkout_hours=None,  # Optional field
        rest_time=None,  # Optional field
        handling_enabled=True,
        zoo_id=1,  # Assumes zoo with ID 1 exists
        description=None,  # Optional field
        tier=1,
        image_filename=None,  # Optional field
        daily_checkout_count=0,
        daily_checkout_duration=timedelta(hours=0),
        last_checkin_time=None,
        checked_in=True,
        status="checked_in"
    )
    
    assert animal_data.name == "Test Lion"
    assert animal_data.species == "Panthera leo"
    assert animal_data.max_daily_checkouts == 1
    assert animal_data.handling_enabled is True
    assert animal_data.zoo_id == 1
    print("✅ AnimalIn object creation successful")
    return animal_data


async def test_animal_creation_from_animal_in():
    """Test that Animal objects can be created from AnimalIn data."""
    animal_in_data = await test_animal_in_creation()
    
    # This is the correct way to create an Animal from AnimalIn
    # (NOT using Animal.model_validate which caused the 422 error)
    animal = Animal(**animal_in_data.model_dump())
    
    assert animal.name == "Test Lion"
    assert animal.species == "Panthera leo"
    assert animal.max_daily_checkouts == 1
    print("✅ Animal object creation from AnimalIn successful")
    return animal


async def test_full_animal_database_lifecycle():
    """Test complete animal creation, save, and deletion cycle."""
    async for session in get_db_session():
        try:
            # Create AnimalIn data
            animal_data = AnimalIn(
                name="Test Database Lion",
                species="Panthera leo",
                max_daily_checkouts=2,
                max_daily_checkout_hours=4,  # With optional field
                rest_time=1.5,  # With optional field  
                handling_enabled=True,
                zoo_id=1,
                description="A test lion for database testing",  # With optional field
                tier=2,
                image_filename=None,
                daily_checkout_count=0,
                daily_checkout_duration=timedelta(hours=0),
                last_checkin_time=None,
                checked_in=True,
                status="checked_in"
            )
            
            # Create Animal object (the correct way)
            db_animal = Animal(**animal_data.model_dump())
            
            # Save to database
            session.add(db_animal)
            await session.commit()
            await session.refresh(db_animal)
            
            # Verify it was saved
            assert db_animal.id is not None
            assert db_animal.name == "Test Database Lion"
            assert db_animal.max_daily_checkout_hours == 4
            assert db_animal.rest_time == 1.5
            assert db_animal.description == "A test lion for database testing"
            
            print(f"✅ Animal saved to database with ID: {db_animal.id}")
            
            # Clean up - delete the test animal
            await session.delete(db_animal)
            await session.commit()
            print("✅ Test animal deleted successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Database lifecycle test failed: {e}")
            await session.rollback()
            return False
        
        break


def run_animal_model_tests():
    """Run all animal model tests."""
    print("=" * 50)
    print("ANIMAL MODEL TESTS")
    print("=" * 50)
    
    # Test 1: AnimalIn creation
    try:
        asyncio.run(test_animal_in_creation())
        print("✅ Test 1 PASSED: AnimalIn creation")
    except Exception as e:
        print(f"❌ Test 1 FAILED: AnimalIn creation - {e}")
        return False
    
    # Test 2: Animal creation from AnimalIn
    try:
        asyncio.run(test_animal_creation_from_animal_in())
        print("✅ Test 2 PASSED: Animal creation from AnimalIn")
    except Exception as e:
        print(f"❌ Test 2 FAILED: Animal creation from AnimalIn - {e}")
        return False
    
    # Test 3: Full database lifecycle
    try:
        success = asyncio.run(test_full_animal_database_lifecycle())
        if success:
            print("✅ Test 3 PASSED: Full database lifecycle")
        else:
            print("❌ Test 3 FAILED: Full database lifecycle")
            return False
    except Exception as e:
        print(f"❌ Test 3 FAILED: Full database lifecycle - {e}")
        return False
    
    print("=" * 50)
    print("✅ ALL ANIMAL MODEL TESTS PASSED")
    print("=" * 50)
    return True


if __name__ == "__main__":
    run_animal_model_tests() 