"""
Test script to check if routes are loaded
"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("Testing Route Registration")
print("=" * 60)

try:
    from app.main import app
    
    print("\n✅ App imported successfully!")
    print(f"\nTotal routes: {len(app.routes)}")
    
    print("\n📋 All registered routes:")
    print("-" * 60)
    
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            methods = ', '.join(route.methods) if route.methods else 'N/A'
            print(f"{methods:10} {route.path}")
    
    print("-" * 60)
    
    # Check for profile routes specifically
    profile_routes = [r for r in app.routes if hasattr(r, 'path') and 'profile' in r.path.lower()]
    
    print(f"\n🔍 Profile routes found: {len(profile_routes)}")
    
    if profile_routes:
        print("✅ Profile routes are registered!")
        for route in profile_routes:
            methods = ', '.join(route.methods) if hasattr(route, 'methods') and route.methods else 'N/A'
            print(f"  {methods:10} {route.path}")
    else:
        print("❌ NO profile routes found!")
        print("\n🔧 This means the router wasn't included properly.")
        print("   Check: app.main line ~101")
        
    # Check imports
    print("\n📦 Checking imports...")
    try:
        from app.api.endpoints import profile, progress, upload
        print("✅ All new endpoints can be imported")
        print(f"   Profile router routes: {len(profile.router.routes)}")
        print(f"   Progress router routes: {len(progress.router.routes)}")
        print(f"   Upload router routes: {len(upload.router.routes)}")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
