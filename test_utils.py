"""
Test suite for the utils module
Tests the centralized utility functions
"""

import os
import asyncio
import tempfile
from utils import ErrorHandler, FileManager, ConfigLoader, DateTimeHelper, get_logger


def test_error_handler():
    """Test ErrorHandler functionality"""
    print("🧪 Test ErrorHandler...")
    
    # Test safe_execute with success
    result = ErrorHandler.safe_execute(lambda: 42, default_return=0)
    assert result == 42, "safe_execute should return function result"
    
    # Test safe_execute with failure
    def failing_func():
        raise ValueError("Test error")
    
    result = ErrorHandler.safe_execute(failing_func, default_return=-1)
    assert result == -1, "safe_execute should return default on error"
    
    print("✅ ErrorHandler: OK")


async def test_file_manager():
    """Test FileManager functionality"""
    print("🧪 Test FileManager...")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        test_content = "Hello, TauroBot!"
        
        # Test ensure_directory
        nested_path = os.path.join(tmpdir, "nested", "dir", "file.txt")
        assert FileManager.ensure_directory(nested_path), "ensure_directory should succeed"
        assert os.path.exists(os.path.dirname(nested_path)), "Directory should be created"
        
        # Test async_write_file
        success = await FileManager.async_write_file(test_file, test_content)
        assert success, "async_write_file should succeed"
        
        # Test file_exists
        assert FileManager.file_exists(test_file), "file_exists should return True"
        
        # Test async_read_file
        content = await FileManager.async_read_file(test_file)
        assert content == test_content, "async_read_file should return correct content"
        
        # Test safe_remove
        assert FileManager.safe_remove(test_file), "safe_remove should succeed"
        assert not FileManager.file_exists(test_file), "File should be removed"
        
        # Test safe_remove on non-existent file
        assert FileManager.safe_remove(test_file), "safe_remove should handle non-existent files"
    
    print("✅ FileManager: OK")


def test_config_loader():
    """Test ConfigLoader functionality"""
    print("🧪 Test ConfigLoader...")
    
    # Test get_env_int
    os.environ['TEST_INT'] = '123'
    assert ConfigLoader.get_env_int('TEST_INT', 0) == 123, "get_env_int should parse integer"
    assert ConfigLoader.get_env_int('NONEXISTENT', 99) == 99, "get_env_int should use default"
    
    # Test invalid int
    os.environ['TEST_INVALID_INT'] = 'not_a_number'
    assert ConfigLoader.get_env_int('TEST_INVALID_INT', 50) == 50, "get_env_int should handle invalid values"
    
    # Test get_env_float
    os.environ['TEST_FLOAT'] = '3.14'
    assert ConfigLoader.get_env_float('TEST_FLOAT', 0.0) == 3.14, "get_env_float should parse float"
    
    # Test get_env_list
    os.environ['TEST_LIST'] = '1,2,3,4,5'
    result = ConfigLoader.get_env_list('TEST_LIST', item_type=int)
    assert result == [1, 2, 3, 4, 5], "get_env_list should parse integer list"
    
    os.environ['TEST_STR_LIST'] = 'a, b, c'
    result = ConfigLoader.get_env_list('TEST_STR_LIST', item_type=str)
    assert result == ['a', 'b', 'c'], "get_env_list should parse string list"
    
    # Cleanup
    for key in ['TEST_INT', 'TEST_INVALID_INT', 'TEST_FLOAT', 'TEST_LIST', 'TEST_STR_LIST']:
        os.environ.pop(key, None)
    
    print("✅ ConfigLoader: OK")


def test_datetime_helper():
    """Test DateTimeHelper functionality"""
    print("🧪 Test DateTimeHelper...")
    
    # Test get_timestamp
    timestamp = DateTimeHelper.get_timestamp()
    assert timestamp is not None, "get_timestamp should return timestamp"
    assert 'T' in timestamp, "Timestamp should be in ISO format"
    
    # Test get_unix_timestamp
    unix_ts = DateTimeHelper.get_unix_timestamp()
    assert isinstance(unix_ts, float), "get_unix_timestamp should return float"
    assert unix_ts > 0, "Unix timestamp should be positive"
    
    # Test timestamp_to_datetime
    test_timestamp = "2024-01-01T12:00:00"
    dt = DateTimeHelper.timestamp_to_datetime(test_timestamp)
    assert dt is not None, "timestamp_to_datetime should return datetime"
    
    print("✅ DateTimeHelper: OK")


def test_get_logger():
    """Test logger configuration"""
    print("🧪 Test get_logger...")
    
    logger = get_logger("test_module")
    assert logger is not None, "get_logger should return logger"
    assert logger.name == "test_module", "Logger should have correct name"
    
    print("✅ get_logger: OK")


async def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("🔧 Utils Module - Test Suite")
    print("="*50 + "\n")
    
    try:
        test_error_handler()
        await test_file_manager()
        test_config_loader()
        test_datetime_helper()
        test_get_logger()
        
        print("\n" + "="*50)
        print("✅ All utils tests completed successfully!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    asyncio.run(main())
