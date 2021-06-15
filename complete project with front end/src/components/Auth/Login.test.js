import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';
import { GlobalProvider, GlobalContext } from '../../context/Provider'

const renderWithContext = (
    component) => {
    return {
        ...render(
            <GlobalProvider value={GlobalContext}>
                {component}
            </GlobalProvider>)
    }
}



test('renders login page', () => {
    renderWithContext(<BrowserRouter>
        <Login authState={{ error: "" }} />
    </BrowserRouter>);
    const headerText = screen.getByText("Social Sprout");
    const formHeading = screen.getByText("Login");
    expect(headerText).toBeInTheDocument();
    expect(formHeading).toBeInTheDocument();
});

test('login page form cannot be submitted if any empty values', () => {
    renderWithContext(<BrowserRouter>
        <Login />
    </BrowserRouter>);
    const headerText = screen.getByText("Social Sprout");
    const formHeading = screen.getByText("Login");
    const input = screen.getByTestId("email")
    const inputPswd = screen.getByTestId("password")

    expect(headerText).toBeInTheDocument();
    expect(formHeading).toBeInTheDocument();
    fireEvent.change(input, { target: { value: " " } })
    fireEvent.change(inputPswd, { target: { value: "riya" } })
});