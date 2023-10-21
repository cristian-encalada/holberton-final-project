import ReactDOM from 'react-dom/client';
import { data } from 'autoprefixer';
import App from './App'
import Header from './Components/Header'
const root = ReactDOM.createRoot(document.getElementById('renderizado'));
root.render(
    <>
        <Header />
        <App />
    </>
);