import FiltersBar from "./FiltersBar"
import Navbar from "./Navbar"
function Header() {
  return (
    <header className="from-azul-600 to-white lg:bg-azul-400 flex h-screen flex-col items-center justify-center bg-opacity-60 bg-gradient-to-b bg-blend-multiply lg:flex lg:h-screen lg:w-full lg:flex-col lg:items-center lg:justify-center lg:bg-[url('https://upload.wikimedia.org/wikipedia/commons/6/60/Atardecer_en_el_Palacio_Legislativo.jpg')] lg:bg-cover lg:bg-center">
      <Navbar/>
      <FiltersBar/>
    </header>
  )
}

export default Header;