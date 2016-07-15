from xwebapp.config import is_debug_mode, is_test_mode
import webapp2

webapp = webapp2.WSGIApplication(debug=is_debug_mode())

if is_test_mode():
    try:
        import app
        routes = app.routes
    except ImportError:
        routes = []
else:
    import app
    routes = app.routes

for route in routes:
    webapp.router.add(route)
