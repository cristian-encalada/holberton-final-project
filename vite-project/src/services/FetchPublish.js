export default async function fetchPublish(pageNumber, currency) {
    try {
        const response = await fetch(`https://alquivago-flask-apis.vercel.app/api/v1/rent/inmuebles?page=${pageNumber}${currency? `&moneda=${currency}`: ''}`);
        
        if (!response.ok) {
            throw new Error('La solicitud no fue exitosa');
        }
        
        const apiData = await response.json();
        return apiData.rents;
    } catch (error) {
        console.error('Error:', error);
        return []; // Devolver un valor por defecto en caso de error
    }
}
