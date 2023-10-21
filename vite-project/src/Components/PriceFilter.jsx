import PropTypes from 'prop-types';
import { useState } from 'react';

export default function PriceFilter({ setCurrencyFilter }) {
PriceFilter.propTypes = {
    setCurrencyFilter: PropTypes.func.isRequired,
};
    const [visible, setVisible] = useState('hidden');

    function handleClick() {
        if (visible === 'flex') {
            setVisible('hidden');
        } else {
            setVisible('flex');
        }
    }

    return (
        <>
        <div className="flex h-32 w-40 flex-col gap-1 rounded-lg bg-white">
        <button id='price-btn' className={`h-1/2 w-full rounded-lg bg-slate-400 font-medium`} onClick={handleClick}>Moneda</button>
        <ul className={`${visible} h-1/2 w-full items-center justify-evenly`}>
          <li className="font-medium">
            <label> <input type="radio" name="currency" value="USD" onClick={(e) => setCurrencyFilter(e.target.value)} /> USD </label>
          </li>
          <li className="font-medium">
            <label> <input type="radio" name="currency" value="UYU" onClick={(e) => setCurrencyFilter(e.target.value)}/> UYU </label>
          </li>
        </ul>
      </div>
      </>
    )
}


