import { useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

export default function TypeButton({ filters, setFilters }) {
  const [visible, setVisible] = useState('invisible')
  const router = useRouter();
  const pathName = usePathname();

  function checkingValue(filterType, valueToCheck) {
    for (const element of filters) {
      if (element.startsWith(filterType)) {
        if (element.includes(valueToCheck)) {
          return true
        }
        return false
      }
    }
  }

  function handleVisibility() {
    if (visible === 'invisible') {
      setVisible('visible')
    } else setVisible('invisible')
  }
  const handleClick = (e) => {
    const value = e.target.value;
    console.log(filters.includes(value))
    if (filters.includes(value)) {
      setFilters(filters.filter((filter) => filter !== value));
    } else {
        setFilters([...filters, value]);
      }
    }
  
  function applyFilters() {
    if (filters.length === 0) {
      if (pathName.includes("moneda=UYU")) {
        return router.push('moneda=UYU')
      }
      else if (pathName.includes("moneda=USD")) {
        return router.push('moneda=USD')
      }
      else {
        return router.push('/publish')
    }
  }
    if (pathName.includes('moneda=UYU')) {
      return router.push(`/publish/moneda=UYU&tipos=${filters.join(',')}`)
    }
    else if (pathName.includes('moneda=USD')) {
      return router.push(`/publish/moneda=USD&tipos=${filters.join(',')}`)
    }
    if (pathName.includes('tipos') && !pathName.includes('moneda')) {
      return router.push(`tipos=${filters.join(',')}`)
    }
  }

  return (
    <div className="flex flex-col w-1/6 gap-1 h-20" onMouseEnter={() => setVisible('visible')} onMouseLeave={() => setVisible('invisible')}>
      <button className="rounded-md font-medium text-lg w-full bg-white shadow py-2 hover:bg-slate-200 transition">Tipo</button>
      <div className={`${visible} flex flex-col w-full border-2 border-slate-300 rounded-lg bg-white shadow-lg`}>
        <ul className="overflow-auto h-32 flex flex-col items-center">
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=0" onChange={handleClick} checked={filters.includes('tipos=0')}/>
            Apartamento
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=4" onChange={handleClick} checked={filters.includes('tipos=4')}/>
            Casa
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=2" onChange={handleClick} checked={filters.includes('tipos=2')}/>
            Local
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=3" onChange={handleClick} checked={filters.includes('tipos=3')}/>
            Oficina
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=5" onChange={handleClick} checked={filters.includes('tipos=5')}/>
            Terreno
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=7" onChange={handleClick} checked={filters.includes('tipos=7')}/>
            Garage
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=6" onChange={handleClick} checked={filters.includes('tipos=6')}/>
            Campo
          </li>
          <li className="py-2 text-lg font-medium hover:bg-slate-200 rounded-lg transition w-full">
            <input  className="w-5"  type="checkbox" value="tipos=9" onChange={handleClick} checked={filters.includes('tipos=9')}/>
            Otro
          </li>
        </ul>
      </div>
    </div>
  );
}
