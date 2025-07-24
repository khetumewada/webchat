#!/usr/bin/env python
"""
Test Redis connection for WebChat
"""
import redis
import sys

def test_redis_connection():
    try:
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Test connection
        r.ping()
        print("✅ Redis connection successful!")
        
        # Test set/get
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        
        if value == b'test_value':
            print("✅ Redis read/write test successful!")
        else:
            print("❌ Redis read/write test failed!")
            
        # Clean up
        r.delete('test_key')
        
        return True
        
    except redis.ConnectionError:
        print("❌ Redis connection failed!")
        print("Make sure Redis server is running:")
        print("   redis-server")
        return False
    except Exception as e:
        print(f"❌ Redis test failed: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Testing Redis connection...")
    if test_redis_connection():
        print("\n🎉 Redis is working correctly!")
    else:
        print("\n💡 To fix Redis issues:")
        print("1. Install Redis: brew install redis (macOS) or apt install redis-server (Ubuntu)")
        print("2. Start Redis: redis-server")
        print("3. Test Redis: redis-cli ping")
        sys.exit(1)
