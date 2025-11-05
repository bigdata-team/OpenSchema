import { Navigate, Outlet, useLocation } from 'react-router';
import { useAuth } from '@/contexts/AuthContext';

interface ProtectedRouteProps {
  redirectTo?: string;
  children?: React.ReactNode;
}

/**
 * ProtectedRoute component that requires authentication
 * Redirects to login if user is not authenticated
 */
export default function ProtectedRoute({
  redirectTo = '/',
  children
}: ProtectedRouteProps) {
  const { isAuthenticated, isInitializing } = useAuth();
  const location = useLocation();

  // Show loading state while checking authentication
  if (isInitializing) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Redirect to specified path if not authenticated
  if (!isAuthenticated) {
    console.log('[ProtectedRoute] User not authenticated, redirecting to:', redirectTo);
    // Save the attempted location for redirecting after login
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Render children if provided, otherwise render Outlet for nested routes
  return children ? <>{children}</> : <Outlet />;
}
