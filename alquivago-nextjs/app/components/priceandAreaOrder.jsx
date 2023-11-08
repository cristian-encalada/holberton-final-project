'use client'
import { useState } from "react"
import mapIcon from '../../public/mapIcon.svg'
import listIcon from '../../public/listIcon.svg'
import Link from "next/link"
import Image from "next/image"
import PriceOrder from "./priceOrder"
import AreaOrder from "./AreaOrder"

export default function OrderingSection() {
  const [orders, setOrders] = useState([])
  return (
    <section className="hidden w-full h-24 gap-2 bg-white md:first-letter md:flex justify-start">
      <PriceOrder orders={orders} setOrders={setOrders}>Ordenar Precio</PriceOrder>
      <AreaOrder orders={orders} setOrders={setOrders}>Ordenar Área</AreaOrder>
        <ul className="flex gap-2 items-start absolute right-2">
          <li><Link href='/map'><Image src={mapIcon} className="w-10 h-10 hover:scale-125 transition" alt="map icon"/></Link> </li>
          <li><Link href='/publish'><Image src={listIcon} className="w-8 h-8 hover:scale-125 transition" alt="map icon"/></Link> </li>
        </ul>
    </section>
  )
}