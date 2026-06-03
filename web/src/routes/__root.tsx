import { createRootRoute, Outlet, Link } from "@tanstack/react-router";
import { Star, Menu, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function Header() {
  const [open, setOpen] = useState(false);

  const navLinks = [
    { to: "/", label: "Inicio" },
    { to: "/como-funciona", label: "Cómo funciona" },
    { to: "/nosotros", label: "Nosotros" },
    { to: "/privacidad", label: "Privacidad" },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-[hsl(var(--border))] bg-[hsl(var(--background))/95] backdrop-blur supports-[backdrop-filter]:bg-[hsl(var(--background))/60]">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl text-[hsl(var(--foreground))]">
            <Star className="h-6 w-6 fill-[hsl(var(--accent))] text-[hsl(var(--accent))]" />
            <span>Mejores<span className="text-[hsl(var(--primary))]">Reseñas</span></span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            {navLinks.map((l) => (
              <Link
                key={l.to}
                to={l.to}
                className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))] transition-colors"
                activeProps={{ className: "text-sm text-[hsl(var(--foreground))] font-medium" }}
              >
                {l.label}
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-3">
            <Button size="sm">Comenzar gratis</Button>
          </div>

          <button
            className="md:hidden p-2"
            onClick={() => setOpen(!open)}
            aria-label="Menú"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {open && (
          <div className="md:hidden py-4 border-t border-[hsl(var(--border))]">
            <nav className="flex flex-col gap-4">
              {navLinks.map((l) => (
                <Link
                  key={l.to}
                  to={l.to}
                  className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]"
                  onClick={() => setOpen(false)}
                >
                  {l.label}
                </Link>
              ))}
              <Button size="sm" className="w-full">Comenzar gratis</Button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="border-t border-[hsl(var(--border))] bg-[hsl(var(--muted))]">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center gap-2 font-bold text-xl mb-3">
              <Star className="h-5 w-5 fill-[hsl(var(--accent))] text-[hsl(var(--accent))]" />
              <span>Mejores<span className="text-[hsl(var(--primary))]">Reseñas</span></span>
            </Link>
            <p className="text-sm text-[hsl(var(--muted-foreground))] max-w-xs">
              Ayudamos a negocios en México a conseguir más reseñas auténticas y mejorar su visibilidad en Google Maps.
            </p>
          </div>
          <div>
            <p className="text-sm font-semibold mb-3">Producto</p>
            <ul className="space-y-2">
              <li><Link to="/como-funciona" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">Cómo funciona</Link></li>
              <li><Link to="/nosotros" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">Nosotros</Link></li>
            </ul>
          </div>
          <div>
            <p className="text-sm font-semibold mb-3">Legal</p>
            <ul className="space-y-2">
              <li><Link to="/privacidad" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">Privacidad</Link></li>
              <li><Link to="/terminos" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">Términos de uso</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-[hsl(var(--border))] flex flex-col sm:flex-row justify-between items-center gap-2">
          <p className="text-xs text-[hsl(var(--muted-foreground))]">© 2026 MejoresReseñas. Todos los derechos reservados.</p>
          <p className="text-xs text-[hsl(var(--muted-foreground))]">Ciudad Juárez, Chihuahua, México · contacto@mejoresreviews.com</p>
        </div>
      </div>
    </footer>
  );
}

export const Route = createRootRoute({
  component: () => (
    <div className={cn("min-h-screen flex flex-col")}>
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  ),
});
