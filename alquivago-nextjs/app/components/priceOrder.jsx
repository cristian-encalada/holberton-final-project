'use client'
import { useState } from "react"
import { usePathname, useRouter} from "next/navigation"
export default function PriceOrder({ children, orders, setOrders }) {
    const [visibleState, setVisibleState] = useState('invisible')
    const pathName = usePathname()
    const router = useRouter()
  
    function handleOrder(e) {
      const value = e.target.value;
      if (!orders.includes(value)) {
        let updatedOrders = orders.filter(order => !order.startsWith('price')); // Eliminar cualquier opción de precio existente
        setOrders([...updatedOrders, value]);
     } else {
        setOrders(orders.filter((order) => order != value))
     }
     setOrders((updatedOrders) => {
      if (pathName === '/publish') {
        return router.push(`${pathName}/-orden=${updatedOrders.join(',')}`);
      }
      else if (pathName === '/') {
        return router.push(`/publish/-orden=${updatedOrders.join(',')}`);
      }
      router.push(`${pathName.split('-')[0]}-orden=${updatedOrders.join(',')}`);
      return updatedOrders
    });
    }
    function handleVisibility() {
      if (visibleState === 'invisible') {
        setVisibleState('visible')
      } else setVisibleState('invisible')
    }
    return (
      <div className="w-1/6 flex justify-center flex-col gap-1 text-azul-600">
      <button className="border-2 font-medium w-full rounded-lg h-1/3 hover:bg-azul-300 hover:scale-105 transition hover:text-white" onClick={handleVisibility}>
        {children}
      </button>
      <div className={`h-2/3 w-full rounded-2xl shadow-2xl ${visibleState}`}>
      <div className="flex w-full h-1/2 items-center justify-center">
        <input type="radio" name="ordenPrecio" id="precioAscendente" className="w-1/12" value='price:1' onClick={handleOrder}/>
        <label htmlFor="precioAscendente" className="w-5/6 hover:bg-azul-100 transition rounded-md">Ascendente</label>
      </div> <div className="flex w-full h-1/2 items-center justify-center">
        <input type="radio" name="ordenPrecio" id="precioDescendente" className="w-1/12" value='price:-1' onClick={handleOrder} />
        <label htmlFor="precioDescendente" className="w-5/6 hover:bg-azul-100 transition rounded-md">Descendente</label>
      </div>
      </div>
      </div>
    )
}