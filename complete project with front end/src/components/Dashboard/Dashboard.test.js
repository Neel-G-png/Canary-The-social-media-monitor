import React from 'react'
import { render, waitFor } from '@testing-library/react'
import { GlobalProvider, GlobalContext } from '../../context/Provider'
import Dashboard from "./index"
import mockedAxios from 'axios';

const renderWithContext = (
    component) => {
    return {
        ...render(
            <GlobalProvider value={GlobalContext}>
                {component}
            </GlobalProvider>)
    }
}


it('should display a loader and then display dashboard', async () => {

    const { getByTestId } = renderWithContext(<Dashboard />)

    expect(getByTestId('loader')).toHaveTextContent('Updating the Dashboard')

})
