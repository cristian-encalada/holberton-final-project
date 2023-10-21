import fetchPublish from "../services/FetchPublish";
import { useState, useEffect } from "react";

export default function useDataRetrieval(initialCurrency) {
    const [data, setData] = useState([]);
    const [page, setPage] = useState(1);

    useEffect(() => {
        setPage(1);
        setData([])
      }, [initialCurrency]);

    useEffect(() => {
        async function fetchDataFromAPI() {
            try {
                const newData = await fetchPublish(page, initialCurrency);
                setData((prevData) => [...prevData, ...newData]);
                if (newData.length == 10) {
                    setPage((prevPage) => prevPage + 1);
                }
                
            } catch (error) {
                console.error(error);
            }
        }
    
        fetchDataFromAPI();
    }, [page, initialCurrency]);
    return { data };
}