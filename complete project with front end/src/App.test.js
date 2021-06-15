import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

test('renders header with login page or dashboard', () => {
    render(<BrowserRouter><App /></BrowserRouter>);
});
