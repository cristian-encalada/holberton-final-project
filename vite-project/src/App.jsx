import { useState } from 'react';
import Publish from './Components/Publish'
import useDataRetrieval from "./hooks/useDataRetrieval";
import PriceFilter from './Components/PriceFilter';

export default function App () {
    const [currencyFilter, setCurrencyFilter] = useState('')
    const { data } = useDataRetrieval(currencyFilter)
    return (
        <section className='flex flex-col justify-center items-center'>
            <PriceFilter setCurrencyFilter={setCurrencyFilter} />
            {data.map((alquiler) => (
                <Publish
                    key={alquiler.id}
                    propertyTitle={alquiler.title || 'Titulo no disponible'}
                    propertyArea={alquiler.total_area}
                    propertyImage={alquiler.images && alquiler.images[0]}
                    propertyBathrooms={alquiler.bathrooms}
                    propertyBedrooms={alquiler.bedrooms}
                    propertyType={alquiler.property_type}
                    propertyCurrency={alquiler.currency}
                    propertyZone={alquiler.zone_name}
                    propertyPrice={alquiler.price}
                    propertyOrigin={alquiler.origin}
                    propertyLink={alquiler.url_link}
                />
            ))}
        </section>
    );
}
