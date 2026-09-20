import React, { useState, lazy, Suspense } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';
import PrivateRoute from './components/common/PrivateRoute';
import { useAuth } from './context/AuthContext';
import PageSkeleton from './components/common/PageSkeleton';

// Lazy-loaded page chunks — only downloaded when navigated to
const Login          = lazy(() => import('./components/Auth/Login'));
const Register       = lazy(() => import('./components/Auth/Register'));
const ChangePassword = lazy(() => import('./components/Auth/ChangePassword'));
const Dashboard      = lazy(() => import('./components/Dashboard/Dashboard'));
const StudentList    = lazy(() => import('./components/Students/StudentList'));
const AddStudent     = lazy(() => import('./components/Students/AddStudent'));
const Attendance     = lazy(() => import('./pages/Attendance'));
const TeacherProfile = lazy(() => import('./components/Profile/TeacherProfile'));
const EditProfile    = lazy(() => import('./components/Profile/EditProfile'));

const App = () => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {!isAuthPage && isAuthenticated && (
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      )}
      <div className={!isAuthPage && isAuthenticated ? 'lg:pl-72' : ''}>
        {!isAuthPage && isAuthenticated && (
          <Navbar onMenuToggle={() => setSidebarOpen(prev => !prev)} />
        )}
        <main className={isAuthPage ? 'min-h-screen' : 'px-4 py-4 sm:px-6 sm:py-6'}>
          <Suspense fallback={<PageSkeleton />}>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Protected Routes */}
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/students" element={
                <PrivateRoute>
                  <StudentList />
                </PrivateRoute>
              } />
              <Route path="/students/add" element={
                <PrivateRoute>
                  <AddStudent />
                </PrivateRoute>
              } />
              <Route path="/attendance" element={
                <PrivateRoute>
                  <Attendance />
                </PrivateRoute>
              } />
              <Route path="/profile" element={
                <PrivateRoute>
                  <TeacherProfile />
                </PrivateRoute>
              } />
              <Route path="/profile/edit" element={
                <PrivateRoute>
                  <EditProfile />
                </PrivateRoute>
              } />
              <Route path="/change-password" element={
                <PrivateRoute>
                  <ChangePassword />
                </PrivateRoute>
              } />

              {/* Redirect root to dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* 404 - Redirect to dashboard */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </div>
  );
};

export default App;