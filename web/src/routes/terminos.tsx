import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/terminos")({
  component: Terminos,
});

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="text-xl font-bold mb-3 text-[hsl(var(--foreground))]">{title}</h2>
      <div className="text-[hsl(var(--muted-foreground))] space-y-3 leading-relaxed text-sm">{children}</div>
    </section>
  );
}

function Terminos() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-16">
      <h1 className="text-4xl font-bold mb-2">Términos de Uso</h1>
      <p className="text-sm text-[hsl(var(--muted-foreground))] mb-12">
        Última actualización: 2 de junio de 2026 · MejoresReseñas · Ciudad Juárez, Chihuahua, México
      </p>

      <Section title="1. Aceptación de los términos">
        <p>Al usar la plataforma MejoresReseñas aceptas estos términos en su totalidad. Si no estás de acuerdo, no uses el servicio.</p>
      </Section>

      <Section title="2. Descripción del servicio">
        <p>
          MejoresReseñas es una plataforma de software que ayuda a negocios locales a gestionar y mejorar su reputación en Google Maps mediante herramientas para solicitar reseñas auténticas, responder reseñas existentes y analizar su visibilidad local.
        </p>
      </Section>

      <Section title="3. Uso permitido">
        <p>Puedes usar MejoresReseñas para:</p>
        <ul className="list-disc pl-5 space-y-1">
          <li>Solicitar reseñas honestas a clientes reales que han tenido una experiencia genuina con tu negocio.</li>
          <li>Gestionar y responder reseñas en tu Perfil de Google Business.</li>
          <li>Analizar datos de búsqueda local para mejorar tu visibilidad.</li>
          <li>Monitorear el crecimiento de tu reputación online.</li>
        </ul>
      </Section>

      <Section title="4. Uso prohibido — Cumplimiento con las políticas de Google">
        <p className="font-medium text-[hsl(var(--foreground))]">Queda estrictamente prohibido usar MejoresReseñas para:</p>
        <ul className="list-disc pl-5 space-y-1">
          <li>Comprar, vender o intercambiar reseñas de ningún tipo.</li>
          <li>Crear reseñas falsas o fabricadas para cualquier negocio.</li>
          <li>Ofrecer incentivos (descuentos, regalos, efectivo) a cambio de reseñas positivas.</li>
          <li>Solicitar reseñas a personas que no han interactuado con tu negocio.</li>
          <li>Usar la plataforma para difamar a competidores.</li>
          <li>Automatizar el envío masivo de solicitudes de reseña que imite comportamiento de spam.</li>
        </ul>
        <p>
          El incumplimiento de estas restricciones puede resultar en la terminación inmediata de tu cuenta y podría violar las políticas de Google, llevando a consecuencias sobre tu Perfil de Google Business.
        </p>
      </Section>

      <Section title="5. Uso de APIs de Google">
        <p>
          MejoresReseñas usa las APIs de Google (Google Ads API y Google Business Profile API) conforme a los términos de servicio de Google. Al usar nuestra plataforma, también aceptas los Términos de Servicio de Google aplicables. No transferimos tus datos de Google a terceros sin tu consentimiento explícito.
        </p>
      </Section>

      <Section title="6. Cuentas y responsabilidad">
        <p>
          Eres responsable de mantener la confidencialidad de tu contraseña y de todas las actividades que ocurran bajo tu cuenta. Debes notificarnos inmediatamente de cualquier uso no autorizado.
        </p>
      </Section>

      <Section title="7. Limitación de responsabilidad">
        <p>
          MejoresReseñas no garantiza que el uso de la plataforma resultará en un número específico de reseñas o en una mejora de posición en Google Maps. Los resultados dependen de múltiples factores fuera de nuestro control, incluyendo las políticas y algoritmos de Google.
        </p>
        <p>
          No somos responsables por cambios en las políticas de Google que afecten el funcionamiento de nuestras integraciones.
        </p>
      </Section>

      <Section title="8. Terminación">
        <p>
          Puedes cancelar tu cuenta en cualquier momento. Nos reservamos el derecho de suspender o terminar cuentas que violen estos términos, las políticas de Google, o que usen la plataforma de manera fraudulenta.
        </p>
      </Section>

      <Section title="9. Modificaciones">
        <p>
          Podemos actualizar estos términos con aviso previo de 15 días por correo electrónico. El uso continuado del servicio constituye aceptación de los términos modificados.
        </p>
      </Section>

      <Section title="10. Ley aplicable">
        <p>
          Estos términos se rigen por las leyes de los Estados Unidos Mexicanos. Cualquier controversia será resuelta en los tribunales competentes de Ciudad Juárez, Chihuahua, México.
        </p>
      </Section>

      <Section title="11. Contacto">
        <p>MejoresReseñas · Ciudad Juárez, Chihuahua, México</p>
        <p>Correo: <a href="mailto:contacto@mejoresreviews.com" className="text-[hsl(var(--primary))] hover:underline">contacto@mejoresreviews.com</a></p>
      </Section>
    </div>
  );
}
