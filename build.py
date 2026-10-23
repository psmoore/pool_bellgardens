#!/usr/bin/env python3
"""Build the Bell Gardens Dreamers Aquatics Center preview (index.html), English and Spanish.
Every visible string is written twice; the page shows one language (?lang=es) and the live
schedule (finder.js) follows it. Run: python3 build.py"""
import html, json

E = html.escape
VIEW = "tCWlfEHlMkThb1CBUvtswc"  # Pool Relay: Dreamers Aquatics Center, lane by lane
CITY = "https://www.bellgardens.org/our-city/about-bell-gardens/aquatic-center"

def b(en, es):
    """A bilingual run of inline HTML (already escaped by the caller where needed)."""
    return f'<span lang="en">{en}</span><span lang="es">{es}</span>'

# Session titles as Pool Relay stores them, and what the Spanish page calls them.
I18N = {
    "Lap Swim": "Nado de vueltas", "Recreation Swim": "Nado recreativo", "Swim Lessons": "Clases de natación",
    "Aqua Aerobics": "Aqua aeróbicos", "Low Impact Aerobics": "Aeróbicos de bajo impacto",
    "Drop-In Water Polo": "Waterpolo libre", "Splash-Ball Water Polo": "Splash-Ball (waterpolo infantil)",
    "Southeast Aquatics Dolphins Swim Team": "Equipo de natación Southeast Aquatics Dolphins",
    "S.T.A.R.S. Swim Program": "Programa de natación S.T.A.R.S.",
    "Closed: Thanksgiving": "Cerrado: Día de Acción de Gracias", "Closed: swim competition": "Cerrado: competencia de natación",
    "In the water now": "En el agua ahora", "until": "hasta las", "Opens": "Abre a las", "from": "desde las",
    "Done for today": "Terminado por hoy", "Next": "Próximo", "Nothing scheduled": "Nada programado", "today": "hoy",
    "No hours published": "Sin horario publicado", "through": "hasta el", "all": "los", "of": "de", "lanes": "carriles",
    "Lap swim": "Vueltas", "Rec swim": "Recreativo", "Water fitness": "Ejercicio acuático", "Lessons & teams": "Clases y equipos",
    "Swim lessons": "Clases de natación", "classes": "clases", "noon": "mediodía",
    "and": "y", "Closed": "Cerrado", "Starts": "Empieza el", "now": "ahora", "now, no reopening date yet": "ahora, sin fecha de reapertura",
    "Nothing scheduled in the next four weeks": "Nada programado en las próximas cuatro semanas", "Also": "También",
    "See the calendar for times.": "Vea el calendario para los horarios.",
    "swim competition": "competencia de natación", "Thanksgiving": "Acción de Gracias",
}

# Program cards: who it's for and what it costs. When it runs is never typed here: each {Title}
# becomes a live span that finder.js fills from that Pool Relay session's bookings.
PROGRAMS = [  # (kind, en title, es title, en body, es body)
    ("lap", "Lap Swim", "Nado de vueltas",
     "Ages 13+. {Lap Swim}. $1 teens and 55+, $2 adults.",
     "13 años o más. {Lap Swim}. $1 adolescentes y mayores de 55, $2 adultos."),
    ("rec", "Recreation Swim", "Nado recreativo",
     "All ages, in the activity pool with the slide. {Recreation Swim}. $1 youth and 55+, $2 adults.",
     "Todas las edades, en la alberca recreativa con tobogán. {Recreation Swim}. $1 jóvenes y mayores de 55, $2 adultos."),
    ("learn", "Swim Lessons", "Clases de natación",
     "6 months to adult. {Swim Lessons}. $35 residents, $45 non-residents. An instructor evaluates each swimmer before registration.",
     "De 6 meses a adultos. {Swim Lessons}. $35 residentes, $45 no residentes. Un instructor evalúa a cada nadador antes de inscribirse."),
    ("fit", "Aqua Aerobics", "Aqua aeróbicos",
     "Ages 13+. {Aqua Aerobics}. $1 teens and 55+, $2 adults.",
     "13 años o más. {Aqua Aerobics}. $1 adolescentes y mayores de 55, $2 adultos."),
    ("fit", "Low Impact Aerobics", "Aeróbicos de bajo impacto",
     "Ages 40+: walking, swimming and gentle dance in the water. {Low Impact Aerobics}. $1 seniors, $2 adults.",
     "Mayores de 40: caminar, nadar y baile suave en el agua. {Low Impact Aerobics}. $1 mayores, $2 adultos."),
    ("learn", "Southeast Aquatics Dolphins", "Equipo Southeast Aquatics Dolphins",
     "Swim team, ages 5–18. {Southeast Aquatics Dolphins Swim Team}. $65/month residents, $95 non-residents.",
     "Equipo de natación, 5 a 18 años. {Southeast Aquatics Dolphins Swim Team}. $65 al mes residentes, $95 no residentes."),
    ("learn", "Water Polo", "Waterpolo",
     "Drop-in, ages 13+, $1–$2: {Drop-In Water Polo}. Splash-Ball, ages 6–13, $35/$45 a month: {Splash-Ball Water Polo}.",
     "Libre, 13 años o más, $1–$2: {Drop-In Water Polo}. Splash-Ball, 6 a 13 años, $35/$45 al mes: {Splash-Ball Water Polo}."),
    ("learn", "S.T.A.R.S. Swim Program", "Programa de natación S.T.A.R.S.",
     "Inclusive swimming for all abilities, age 1 to adult, in 30-minute classes. {S.T.A.R.S. Swim Program}. $95.",
     "Natación inclusiva para todas las capacidades, de 1 año a adultos, en clases de 30 minutos. {S.T.A.R.S. Swim Program}. $95."),
]
def live_when(text):
    """Escape a card body and turn each {Pool Relay session title} into a live span."""
    out, rest = "", text
    while "{" in rest:
        pre, rest = rest.split("{", 1)
        title, rest = rest.split("}", 1)
        out += E(pre) + f'<span data-live="when" data-view="{VIEW}" data-pool="dreamers" data-title="{E(title)}">…</span>'
    return out + E(rest)
cards = "".join(f'<div class="program"><h3><span class="k k-{k}"></span>{b(E(t1), E(t2))}</h3><p>{b(live_when(d1), live_when(d2))}</p></div>'
                for k, t1, t2, d1, d2 in PROGRAMS)

REPLACES = [
    ("<b>“Coming soon,” a year after opening.</b> The city's Aquatics Center page still opens on construction: “The new Aquatics Center at Ford Park is coming soon! Updates as of August 25, 2025.” It ends by saying programs continue at Chet Holifield Pool in Montebello.",
     "<b>“Próximamente,” un año después de abrir.</b> La página del centro todavía empieza con la construcción: “¡El nuevo Centro Acuático en Ford Park llegará pronto! Actualizado al 25 de agosto de 2025.” Al final dice que los programas siguen en la alberca Chet Holifield de Montebello."),
    ("<b>A schedule you can't read.</b> The whole fall schedule is one picture of two brochure pages. It can't be searched, zoomed cleanly on a phone, read aloud by a screen reader, or translated.",
     "<b>Un horario que no se puede leer.</b> Todo el horario de otoño es una sola imagen de dos páginas del folleto. No se puede buscar, ampliar bien en el teléfono, leer con un lector de pantalla ni traducir."),
    ("<b>“Click below to read in English and Spanish.”</b> The link goes to the city's home page, and the picture below it is in English only. In a city where most residents speak Spanish at home, this page switches languages with one tap.",
     "<b>“Haga clic abajo para leer en inglés y español.”</b> El enlace lleva a la página principal de la ciudad, y la imagen de abajo solo está en inglés. En una ciudad donde la mayoría habla español en casa, esta página cambia de idioma con un toque."),
    ("<b>Four names, three places.</b> The pool is the “Aquatics Center,” “Dreamer's Aquatic Center,” “John Anson Ford Park Dreamers Aquatics Center” and “Regional Aquatics Center”. Its schedule is filed under Our City › About Bell Gardens, while lessons and rec swim are under Government › City Departments. The lessons page has fees and registration dates but no class times.",
     "<b>Cuatro nombres, tres lugares.</b> La alberca aparece como “Aquatics Center”, “Dreamer's Aquatic Center”, “John Anson Ford Park Dreamers Aquatics Center” y “Regional Aquatics Center”. El horario está en Nuestra Ciudad › Acerca de Bell Gardens, y las clases y el nado recreativo en Gobierno › Departamentos. La página de clases tiene precios y fechas de inscripción, pero no horarios."),
    ("<b>Who's in which water, and when.</b> On weekday evenings, lap swim shares the competition pool with the Dolphins swim team, Splash-Ball and water polo. The brochure lists each one separately and never says how the pool is divided. Here every program has its place, and the lane split is our estimate until the city publishes its own.",
     "<b>Quién está en cada alberca, y cuándo.</b> En las tardes entre semana, el nado de vueltas comparte la alberca de competencia con el equipo Dolphins, Splash-Ball y waterpolo. El folleto los enumera por separado y nunca dice cómo se divide la alberca. Aquí cada programa tiene su lugar; la división de carriles es nuestra estimación hasta que la ciudad publique la suya."),
    ("<b>One schedule, kept current.</b> The city enters each program once. This page, the week table, the lane calendar and the “open now” card update together, and a closure shows here the day it's entered.",
     "<b>Un solo horario, siempre al día.</b> La ciudad registra cada programa una vez. Esta página, la tabla de la semana, el calendario por carriles y el aviso de “abierto ahora” se actualizan juntos, y un cierre aparece aquí el mismo día."),
]
replaces = "".join(f"<li>{b(en, es)}</li>" for en, es in REPLACES)

POOLS = json.dumps([dict(slug="dreamers", name="Dreamers Aquatics Center", area="Bell Gardens", kind="yearRound",
                         address="7950 Scout Ave, Bell Gardens, CA 90201", phone="(562) 806-7665", lat=33.9688, lng=-118.1523,
                         facility="Dreamers Aquatics Center", href="#", hideHead=True)])

doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a City of Bell Gardens website. A mock-up of {CITY}
     with the Dreamers Aquatics Center on one live Pool Relay schedule, in English and Spanish. -->
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Dreamers Aquatics Center | Bell Gardens preview</title>
<script>
  // ?lang=es shows the Spanish page; the choice is remembered for the next visit.
  (function () {{
    var q = new URLSearchParams(location.search).get("lang"), saved = null;
    try {{ saved = localStorage.getItem("bg-lang"); }} catch (e) {{}}
    var lang = q || saved || "en";
    try {{ if (q) localStorage.setItem("bg-lang", q); }} catch (e) {{}}
    // data-lang drives what is shown; lang is for screen readers. Chrome's translator rewrites
    // lang (and would flip the page back), so visibility never depends on it.
    lang = lang === "es" ? "es" : "en";
    document.documentElement.lang = lang;
    document.documentElement.setAttribute("data-lang", lang);
    window.LANG = lang;
  }})();
  window.I18N = {json.dumps(I18N, ensure_ascii=False)};
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="preview-note">{b('<b>Unofficial preview.</b> Not a City of Bell Gardens page &mdash; a mock-up of <a href="' + CITY + '" target="_blank" rel="noopener noreferrer">the Aquatics Center page</a> with the pool on one live schedule.',
                             '<b>Vista previa no oficial.</b> No es una página de la Ciudad de Bell Gardens &mdash; una maqueta de <a href="' + CITY + '" target="_blank" rel="noopener noreferrer">la página del Centro Acuático</a> con la alberca en un horario en vivo.')}</div>
<div class="util"><div class="in"><span>{b('View Agendas', 'Ver agendas')}</span><span>{b('City Council Meetings', 'Juntas del Concejo')}</span><span>{b('Talk to Us', 'Contáctenos')}</span><span>Measure W</span>
  <a class="lang-en" href="?lang=es">En Español</a><a class="lang-es" href="?lang=en">In English</a></div></div>
<header class="site"><div class="hdr">
  <a class="brand" href="#"><img src="https://www.bellgardens.org/Project/Contents/Main/_gfx/cmn/logo.png" alt="City of Bell Gardens, California" onerror="this.parentNode.classList.add('noimg')"><span class="wm"><small>CITY OF</small><b>BELL GARDENS</b><i>California</i></span></a>
  <nav class="nav" aria-label="Main"><span>{b('Services', 'Servicios')}</span><span class="on">{b('Our City', 'Nuestra Ciudad')}</span><span>{b('Government', 'Gobierno')}</span><span>{b('Business', 'Negocios')}</span><span>{b('I Want To…', 'Quiero…')}</span></nav>
</div></header>
<div class="banner"><img src="https://www.bellgardens.org/home/showpublishedimage/4969/638962328297070000" alt="" onerror="this.remove()"><div class="bt">Dreamers Aquatics Center</div></div>

<div class="wrap"><div class="cols">
  <nav class="menu" aria-label="About Bell Gardens">
    <a class="top" href="#">{b('About Bell Gardens', 'Acerca de Bell Gardens')}</a>
    <a href="#">Bell Gardens</a><a href="#">{b('Document Central', 'Documentos')}</a><a href="#">{b('Media Suite', 'Medios')}</a>
    <a href="#">{b('Municipal Code', 'Código Municipal')}</a><a href="#">{b('Calendar', 'Calendario')}</a>
    <a class="here" href="#">{b('Aquatics Center', 'Centro Acuático')}</a>
    <a class="sub" href="#now">{b('Open now', 'Abierto ahora')}</a><a class="sub" href="#week">{b('This week', 'Esta semana')}</a>
    <a class="sub" href="#lanes">{b('Lane by lane', 'Por carril')}</a><a class="sub" href="#programs">{b('Programs & fees', 'Programas y precios')}</a>
    <a href="#">{b('Talk to Us', 'Contáctenos')}</a>
  </nav>
  <main class="sheet">
    <div class="crumbs">{b('Our City » About Bell Gardens', 'Nuestra Ciudad » Acerca de Bell Gardens')}</div>
    <h1>Dreamers Aquatics Center</h1>
    <p class="sub-h">{b('John Anson Ford Park', 'Parque John Anson Ford')} · 7950 Scout Ave, Bell Gardens, CA 90201 · <b>(562) 806-POOL (7665)</b></p>

    <div class="top2">
      <section class="now" id="now" aria-live="polite">
        <h2>{b('Right now', 'Ahora mismo')}</h2>
        <div id="today" data-view="{VIEW}" data-pool="dreamers"><p class="muted">{b('Loading today’s schedule…', 'Cargando el horario de hoy…')}</p></div>
      </section>
      <aside class="hours">
        <h2>{b('Hours', 'Horario')}</h2>
        <div data-live="hours" data-format="dl" data-view="{VIEW}" data-pool="dreamers"><p class="muted">…</p></div>
        <p class="closed" data-live="closures" data-view="{VIEW}" data-pool="dreamers" hidden></p>
        <p class="muted small">{b('First visit? Everyone signs a waiver. Children under 48 inches or under 6 swim with a parent or guardian. Bring your own lock.', '¿Primera visita? Todos firman una exención. Menores de 48 pulgadas o de 6 años nadan con su padre, madre o tutor. Traiga su propio candado.')}</p>
      </aside>
    </div>

    <h2 id="week-h">{b('This week', 'Esta semana')}</h2>
    <div id="week" data-view="{VIEW}"><p class="muted">{b('Loading the week…', 'Cargando la semana…')}</p></div>

    <h2 id="lanes">{b('Lane by lane', 'Por carril')}</h2>
    <p class="muted small">{b('Three heated pools: a 50-meter competition pool, an activity pool with a slide and zero-depth entry, and a warm therapy pool. Tap a day to see who is in which lane.',
                              'Tres albercas con calefacción: una de competencia de 50 metros, una recreativa con tobogán y entrada sin profundidad, y una terapéutica de agua templada. Toque un día para ver quién está en cada carril.')}</p>
    <div class="frame"><iframe src="https://www.poolrelay.com/embed/{VIEW}" height="780" title="Dreamers Aquatics Center, lane by lane" loading="lazy"></iframe></div>

    <h2 id="programs">{b('Programs & fees', 'Programas y precios')}</h2>
    <div class="programs">{cards}</div>
    <p class="muted small">{b('Times on this page come from the live schedule, the same one as the calendar above. Resident registration for lessons opens before open registration; open registration is the first day of class.',
                              'Los horarios de esta página vienen del horario en vivo, el mismo del calendario de arriba. La inscripción para residentes abre antes de la inscripción general, que es el primer día de clase.')}</p>

    <div class="replaces">
      <h2>{b('What this replaces', 'Lo que esto reemplaza')}</h2>
      <ul>{replaces}</ul>
    </div>

    <details class="history"><summary>{b('Building the Aquatics Center: costs, funding and construction updates', 'La construcción del Centro Acuático: costos, fondos y avances')}</summary>
      <p>{b('The City awarded the construction contract to Bernards Bros. Inc. on January 22, 2024 ($26,334,000), for an estimated total project cost of $31.27 million: $3.17 million in CDBG funds, $6 million from the Land and Water Conservation Fund (State Parks), $2 million from Assemblymember Cristina Garcia, $1.5 million from HUD, $4 million from Supervisor Janice Hahn, and $14.6 million from the City’s General Fund.',
             'La Ciudad otorgó el contrato de construcción a Bernards Bros. Inc. el 22 de enero de 2024 ($26,334,000), con un costo total estimado de $31.27 millones: $3.17 millones de fondos CDBG, $6 millones del Land and Water Conservation Fund (Parques Estatales), $2 millones de la asambleísta Cristina Garcia, $1.5 millones de HUD, $4 millones de la supervisora Janice Hahn y $14.6 millones del Fondo General de la Ciudad.')}</p>
      <p>{b('Construction ran from the Notice to Proceed on April 9, 2024 to the grand opening in fall 2025. The construction photo and video log stays on the city’s page.',
             'La construcción comenzó con la orden de inicio del 9 de abril de 2024 y terminó con la gran inauguración en el otoño de 2025. El registro de fotos y videos sigue en la página de la ciudad.')}</p>
    </details>
  </main>
</div></div>
<footer class="site"><div class="in">
  <div><h4>City of Bell Gardens</h4><p>7100 Garfield Ave<br>Bell Gardens, CA 90201<br>(562) 806-7700</p></div>
  <div><h4>{b('Aquatics Center', 'Centro Acuático')}</h4><p>7950 Scout Ave<br>(562) 806-POOL (7665)</p></div>
  <div><h4>{b('About this preview', 'Sobre esta vista previa')}</h4><p>{b('Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with the City of Bell Gardens. Schedule read from the city’s fall 2026 brochure on October 22, 2026.',
                                                                            'Hecha para mostrar horarios de <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a>. No la opera ni está afiliada a la Ciudad de Bell Gardens. Horario tomado del folleto de otoño 2026 de la ciudad el 22 de octubre de 2026.')}</p></div>
</div></footer>
<script>window.POOLS = {POOLS};</script>
<script src="finder.js"></script>
</body>
</html>
"""
open("index.html", "w").write(doc)
print("built index.html")
