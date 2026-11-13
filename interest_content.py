"""Localized international interest pages and a visitor-controlled WhatsApp draft."""
import html
from urllib.parse import urlencode

WHATSAPP = "13053179940"
PHONE = "+1 305-317-9940"


def wa(message="Hi Sparked Live, I'd like to learn more."):
    return "https://wa.me/" + WHATSAPP + "?" + urlencode({"text": message})


COPY = {
    "en": {
        "home": "Home", "apply": "Apply", "international": "International",
        "managers": "Work with us", "contact": "Message us", "privacy": "Privacy",
        "terms": "Terms", "skip": "Skip to content", "form_title": "Start a conversation",
        "intro": "Prepare a short introduction, review it, then send it in WhatsApp. No email required.",
        "name": "Your name", "country": "Where do you live?", "language": "Preferred language",
        "handle": "TikTok handle", "handle_hint": "Creators: enter your @handle. Managers: optional if you do not use TikTok.",
        "role": "I am interested as a", "creator": "Creator", "manager": "Local manager",
        "recruiter": "Recruiter", "brand": "Brand or partner", "program": "Program",
        "live": "LIVE — streaming and community", "shop": "Shop — product content and affiliates",
        "both": "Both LIVE and Shop", "choose": "Choose an option", "other": "Another country",
        "other_language": "Another language",
        "details": "Experience, availability or questions (optional)",
        "details_hint": "Managers: include your country, relevant results, weekly availability and proposed rate. Creators: tell us what you make and what support you want.",
        "adult": "I am 18 or older.",
        "consent": "I would like Sparked to reply about this inquiry. I understand this is an expression of interest, not enrollment or a job offer.",
        "privacy_note": "Your draft stays on this page until you open WhatsApp. It is not saved by this form. WhatsApp processes the text when you open it; Sparked receives it when you send. Privacy policy (English).",
        "prepare": "Prepare my WhatsApp message", "review": "Review your message",
        "review_hint": "Nothing has been sent. Open WhatsApp to review the recipient and send your message there.",
        "open": "Open WhatsApp to send", "fallback": "Prefer to write your own message?",
        "direct": "Message Sparked on WhatsApp", "nojs": "This message builder needs JavaScript. You can contact us directly on WhatsApp below.",
        "status": "Expressions of interest open", "status_title": "Planning our expansion",
        "status_copy": "Sparked is exploring UK, Brazil and Mexico opportunities. Our existing US LIVE operation does not establish approval in these markets. Regional LIVE and Shop participation must each be confirmed before onboarding. Registering interest does not guarantee launch, acceptance, work or earnings.",
        "next_title": "What happens next", "next": ["Tell us your country, program and experience.", "We discuss fit and the current status of the local opportunity.", "If a suitable opportunity becomes available, we explain eligibility and written terms before you decide."],
        "live_title": "For LIVE creators", "live_copy": "Interested in streaming coaching, community building, stream setup and creator collaborations? Tell us about your LIVE experience and the support you need.",
        "shop_title": "For Shop creators", "shop_copy": "Interested in product videos, LIVE shopping or affiliate collaborations? Tell us your niche and relevant experience. Shop is a separate program from LIVE gifting, with its own eligibility and commercial terms.",
        "manager_title": "Help build the local team", "manager_copy": "We welcome inquiries from local managers and recruiters with creator relationships, language skills and relevant experience. Share a proposed scope and rate; any paid work needs a separate written agreement.",
        "footer_status": "UK, Brazil and Mexico: expressions of interest only. LIVE and Shop approvals are separate.",
        "territory_notice": "Sparked is exploring this market and is not claiming an approved local TikTok LIVE network or Shop agency. TikTok is a trademark of its owner.",
    },
    "pt-BR": {
        "home": "Início", "apply": "Participar", "international": "Internacional",
        "managers": "Trabalhe conosco", "contact": "Fale conosco", "privacy": "Privacidade (inglês)",
        "terms": "Termos (inglês)", "skip": "Ir para o conteúdo", "form_title": "Vamos conversar",
        "intro": "Prepare uma breve apresentação, revise e envie pelo WhatsApp. Não é necessário informar e-mail.",
        "name": "Seu nome", "country": "Onde você mora?", "language": "Idioma de preferência",
        "handle": "Perfil no TikTok", "handle_hint": "Criadores: informe seu @perfil. Gestores: opcional se você não usa o TikTok.",
        "role": "Tenho interesse como", "creator": "Criador de conteúdo", "manager": "Gestor local",
        "recruiter": "Recrutador", "brand": "Marca ou parceiro", "program": "Programa",
        "live": "LIVE — transmissões e comunidade", "shop": "Shop — conteúdo de produtos e afiliados",
        "both": "LIVE e Shop", "choose": "Selecione uma opção", "other": "Outro país",
        "other_language": "Outro idioma",
        "details": "Experiência, disponibilidade ou dúvidas (opcional)",
        "details_hint": "Gestores: inclua país, resultados relevantes, disponibilidade semanal e valor proposto. Criadores: conte o que você produz e de qual apoio precisa.",
        "adult": "Tenho 18 anos ou mais.",
        "consent": "Gostaria de receber uma resposta da Sparked sobre esta consulta. Entendo que isto é uma manifestação de interesse, não uma adesão à rede ou oferta de trabalho.",
        "privacy_note": "Seu rascunho fica nesta página até você abrir o WhatsApp. Este formulário não o salva. O WhatsApp processa o texto ao ser aberto; a Sparked o recebe quando você envia. Política de privacidade em inglês.",
        "prepare": "Preparar mensagem para o WhatsApp", "review": "Revise sua mensagem",
        "review_hint": "Nada foi enviado. Abra o WhatsApp, confira o destinatário e envie a mensagem por lá.",
        "open": "Abrir o WhatsApp para enviar", "fallback": "Prefere escrever sua própria mensagem?",
        "direct": "Fale com a Sparked pelo WhatsApp", "nojs": "Este formulário precisa de JavaScript. Você também pode falar conosco pelo link do WhatsApp abaixo.",
        "status": "Recebendo manifestações de interesse", "status_title": "Planejando nossa expansão",
        "status_copy": "A Sparked está avaliando oportunidades no Reino Unido, no Brasil e no México. Nossa operação de LIVE nos EUA não representa aprovação nesses mercados. A participação regional em LIVE e Shop precisa ser confirmada separadamente antes da entrada de criadores. Manifestar interesse não garante lançamento, aceitação, trabalho ou ganhos.",
        "next_title": "Próximos passos", "next": ["Conte seu país, programa de interesse e experiência.", "Conversamos sobre seu perfil e o estágio atual da oportunidade local.", "Se surgir uma oportunidade adequada, explicamos os critérios e os termos por escrito antes de você decidir."],
        "live_title": "Para criadores de LIVE", "live_copy": "Tem interesse em orientação para transmissões, construção de comunidade, configuração técnica e colaborações? Conte sua experiência com LIVE e de qual apoio precisa.",
        "shop_title": "Para criadores de Shop", "shop_copy": "Tem interesse em vídeos de produtos, vendas ao vivo ou parcerias de afiliados? Conte seu nicho e experiência. Shop é um programa separado dos presentes de LIVE, com critérios e condições comerciais próprios.",
        "manager_title": "Ajude a construir a equipe local", "manager_copy": "Queremos conversar com gestores e recrutadores locais que tenham experiência, conhecimento do mercado e relacionamento com criadores. Envie uma proposta de escopo e valor. Qualquer trabalho remunerado exige um acordo separado por escrito.",
        "footer_status": "Reino Unido, Brasil e México: apenas manifestações de interesse. As aprovações de LIVE e Shop são separadas.",
        "territory_notice": "A Sparked está avaliando este mercado e não afirma ter uma rede local de TikTok LIVE ou agência de Shop aprovada. TikTok é uma marca de seu respectivo titular.",
    },
    "es-MX": {
        "home": "Inicio", "apply": "Participar", "international": "Internacional",
        "managers": "Trabaja con nosotros", "contact": "Contáctanos", "privacy": "Privacidad (inglés)",
        "terms": "Términos (inglés)", "skip": "Ir al contenido", "form_title": "Conversemos",
        "intro": "Prepara una breve presentación, revísala y envíala por WhatsApp. No necesitas correo electrónico.",
        "name": "Tu nombre", "country": "¿Dónde vives?", "language": "Idioma de preferencia",
        "handle": "Usuario de TikTok", "handle_hint": "Creadores: escribe tu @usuario. Managers: opcional si no usas TikTok.",
        "role": "Me interesa participar como", "creator": "Creador de contenido", "manager": "Manager local",
        "recruiter": "Reclutador", "brand": "Marca o socio", "program": "Programa",
        "live": "LIVE — transmisiones y comunidad", "shop": "Shop — contenido de productos y afiliados",
        "both": "LIVE y Shop", "choose": "Selecciona una opción", "other": "Otro país",
        "other_language": "Otro idioma",
        "details": "Experiencia, disponibilidad o preguntas (opcional)",
        "details_hint": "Managers: incluye país, resultados relevantes, disponibilidad semanal y tarifa propuesta. Creadores: cuéntanos qué contenido haces y qué apoyo buscas.",
        "adult": "Tengo 18 años o más.",
        "consent": "Quiero que Sparked responda a esta consulta. Entiendo que esto es una expresión de interés, no una incorporación a la red ni una oferta de trabajo.",
        "privacy_note": "Tu borrador permanece en esta página hasta que abres WhatsApp. Este formulario no lo guarda. WhatsApp procesa el texto al abrirlo; Sparked lo recibe cuando lo envías. Política de privacidad en inglés.",
        "prepare": "Preparar mi mensaje de WhatsApp", "review": "Revisa tu mensaje",
        "review_hint": "No se ha enviado nada. Abre WhatsApp, revisa el destinatario y envía el mensaje allí.",
        "open": "Abrir WhatsApp para enviar", "fallback": "¿Prefieres escribir tu propio mensaje?",
        "direct": "Habla con Sparked por WhatsApp", "nojs": "Este formulario necesita JavaScript. También puedes contactarnos con el enlace de WhatsApp de abajo.",
        "status": "Recibimos expresiones de interés", "status_title": "Planeando nuestra expansión",
        "status_copy": "Sparked está explorando oportunidades en el Reino Unido, Brasil y México. Nuestra operación de LIVE en EE. UU. no implica aprobación en estos mercados. La participación regional en LIVE y Shop debe confirmarse por separado antes de incorporar creadores. Registrar tu interés no garantiza lanzamiento, aceptación, trabajo ni ingresos.",
        "next_title": "Qué sigue", "next": ["Cuéntanos tu país, programa de interés y experiencia.", "Conversamos sobre tu perfil y el estado actual de la oportunidad local.", "Si surge una oportunidad adecuada, explicamos los requisitos y las condiciones por escrito antes de que decidas."],
        "live_title": "Para creadores de LIVE", "live_copy": "¿Buscas orientación para transmitir, construir comunidad, configurar tu equipo o colaborar con otros creadores? Cuéntanos tu experiencia en LIVE y qué apoyo necesitas.",
        "shop_title": "Para creadores de Shop", "shop_copy": "¿Te interesan los videos de productos, las ventas en vivo o las colaboraciones de afiliados? Cuéntanos tu nicho y experiencia. Shop es un programa separado de los regalos de LIVE, con sus propios requisitos y condiciones comerciales.",
        "manager_title": "Ayuda a formar el equipo local", "manager_copy": "Queremos conversar con managers y reclutadores locales con experiencia, conocimiento del mercado y relaciones con creadores. Comparte una propuesta de alcance y tarifa. Todo trabajo remunerado requiere un acuerdo separado por escrito.",
        "footer_status": "Reino Unido, Brasil y México: solo expresiones de interés. Las aprobaciones de LIVE y Shop son independientes.",
        "territory_notice": "Sparked está explorando este mercado y no afirma tener una red local de TikTok LIVE ni una agencia de Shop aprobada. TikTok es una marca de su respectivo titular.",
    },
}

MARKETS = {
    "uk": {"name": "United Kingdom", "lang": "en", "title": "Your next chapter as a creator.", "lede": "UK creators, local managers and recruiters: help shape Sparked’s next market. Tell us whether LIVE, Shop or both fit your ambitions.", "message": "Hi Sparked Live, I would like to register interest in your UK expansion."},
    "brazil": {"name": "Brasil", "lang": "pt-BR", "title": "Seu próximo passo como criador.", "lede": "Criadores, gestores e recrutadores no Brasil: queremos conhecer vocês. Conte se seu interesse é em LIVE, Shop ou nos dois programas.", "message": "Olá, Sparked Live! Gostaria de manifestar interesse na expansão para o Brasil."},
    "mexico": {"name": "México", "lang": "es-MX", "title": "Tu siguiente paso como creador.", "lede": "Creadores, managers y reclutadores en México: queremos conocerlos. Cuéntanos si te interesa LIVE, Shop o ambos programas.", "message": "¡Hola, Sparked Live! Me gustaría registrar mi interés en la expansión a México."},
}


def e(value):
    return html.escape(value, quote=True)


def interest_form(u, lang="en", country="", message=None, managers=False, shop=False):
    c = COPY[lang]
    message = message or ("Hi Sparked Live, I would like to discuss a manager or recruiter opportunity." if managers else "Hi Sparked Live, I would like to discuss a creator opportunity.")

    def text_field(name, label, required=False, hint="", maximum=100):
        pattern = r'.*\S.*'
        return f'<div class="f"><label for="{name}">{e(label)}{" *" if required else ""}</label><input id="{name}" name="{name}" type="text" pattern="{pattern}" maxlength="{maximum}" data-message-label="{e(label)}" {"required" if required else ""}{" autocomplete=name" if name == "name" else ""}{f" aria-describedby={name}-hint" if hint else ""}>{f"<small id={name}-hint class=hint>{e(hint)}</small>" if hint else ""}</div>'

    def select(name, label, options, selected=""):
        choices = f'<option value="">{e(c["choose"])}</option>' + "".join(f'<option value="{e(value)}"{" selected" if value == selected else ""}>{e(text)}</option>' for value, text in options)
        return f'<div class="f"><label for="{name}">{e(label)} *</label><select id="{name}" name="{name}" required data-message-label="{e(label)}">{choices}</select></div>'

    country_names = {"en": ["United States", "United Kingdom", "Brazil", "Mexico"], "pt-BR": ["Estados Unidos", "Reino Unido", "Brasil", "México"], "es-MX": ["Estados Unidos", "Reino Unido", "Brasil", "México"]}[lang]
    countries = list(zip(["US", "UK", "BR", "MX"], country_names)) + [("other", c["other"])]
    roles = [(key, c[key]) for key in (["manager", "recruiter"] if managers else ["creator", "manager", "recruiter", "brand"])]
    programs = [("shop", c["shop"])] if shop else [(key, c[key]) for key in ["live", "shop", "both"]]
    fields = text_field("name", c["name"], True) + select("country", c["country"], countries, country)
    fields += select("language", c["language"], [("en", "English"), ("pt", "Português"), ("es", "Español"), ("other", c["other_language"])], {"en": "en", "pt-BR": "pt", "es-MX": "es"}[lang])
    fields += select("role", c["role"], roles) + select("program", c["program"], programs, "shop" if shop else "")
    fields += text_field("handle", c["handle"], hint=c["handle_hint"], maximum=60)
    return f'''<section id="interest" class="interest-panel">
<h2>{e(c['form_title'])}</h2><p>{e(c['intro'])}</p>
<form class="apply" data-interest-form data-whatsapp="{WHATSAPP}" data-message="{e(message)}" onsubmit="return false">
<div class="form-grid">{fields}</div>
<div class="f"><label for="details">{e(c['details'])}</label><textarea id="details" name="details" maxlength="600" data-message-label="{e(c['details'])}" aria-describedby="details-hint"></textarea><small class="hint" id="details-hint">{e(c['details_hint'])}</small></div>
<div class="f consent"><input id="adult" type="checkbox" required><label for="adult">{e(c['adult'])}</label></div>
<div class="f consent"><input id="consent" type="checkbox" required><label for="consent">{e(c['consent'])}</label></div>
<p class="hint">{e(c['privacy_note'])} <a href="{u('/privacy/')}">{e(c['privacy'])}</a></p>
<button type="submit" data-prepare disabled>{e(c['prepare'])}</button>
<section class="message-review" data-review hidden aria-live="polite"><h3>{e(c['review'])}</h3><p>{e(c['review_hint'])}</p>
<label for="draft">{e(c['review'])}</label><textarea id="draft" data-draft readonly rows="8"></textarea>
<a class="btn whatsapp" data-whatsapp-link rel="noopener noreferrer" target="_blank">{e(c['open'])}</a><p>{PHONE}</p></section>
</form>
<noscript><p>{e(c['nojs'])}</p></noscript>
<p>{e(c['fallback'])} <a href="{e(wa(message))}" rel="noopener noreferrer" target="_blank">{e(c['direct'])}</a>.</p>
</section><script src="{u('/assets/interest.js')}" defer></script>'''


def market_cards(u):
    return '<div class="market-list">' + "".join(f'<a class="market-link" href="{u("/" + slug + "/")}"><span><strong>{e(m["name"])}</strong><small>{e(COPY[m["lang"]]["status"])}</small></span><span aria-hidden="true">↗</span></a>' for slug, m in MARKETS.items()) + '</div>'


def country_body(slug, u):
    m = MARKETS[slug]
    c = COPY[m["lang"]]
    cards = ''.join(f'<article class="card"><h2>{e(c[k + "_title"])}</h2><p>{e(c[k + "_copy"])}</p></article>' for k in ['live', 'shop', 'manager'])
    steps = ''.join(f'<li>{e(step)}</li>' for step in c['next'])
    return f'''<section class="hero"><p class="eyebrow">Sparked Live / {e(m['name'])}</p><span class="badge">{e(c['status'])}</span><h1>{e(m['title'])}</h1><p class="lede">{e(m['lede'])}</p><a class="btn" href="#interest">{e(c['form_title'])}</a></section>
<aside class="note"><strong>{e(c['status_title'])}.</strong> {e(c['status_copy'])}</aside>
<div class="grid program-grid">{cards}</div><h2>{e(c['next_title'])}</h2><ol class="steps">{steps}</ol>
{interest_form(u, m['lang'], {'uk': 'UK', 'brazil': 'BR', 'mexico': 'MX'}[slug], m['message'])}
<nav class="country-nav" aria-label="Markets"><a href="{u('/international/')}">International / Internacional</a> · <a href="{u('/uk/')}">UK — English</a> · <a href="{u('/brazil/')}">Brasil — Português</a> · <a href="{u('/mexico/')}">México — Español</a></nav>'''


def international_body(u):
    c = COPY['en']
    return f'''<section class="hero"><span class="badge">Our next chapter</span><h1>Local creators.<br>New connections.</h1><p class="lede">We’re exploring Sparked’s expansion into the UK, Brazil and Mexico. Connect with us as a creator, local manager or recruiter.</p><a class="btn" href="#markets">Choose your country</a></section>
<aside class="note"><strong>{c['status_title']}.</strong> {c['status_copy']}</aside>
<h2 id="markets">Where do you create?</h2>{market_cards(u)}
<div class="grid"><article class="card"><h2>LIVE</h2><p>Streaming, community, technical setup and creator coaching. Each regional network needs its own confirmation before onboarding.</p></article><article class="card"><h2>Shop</h2><p>Product content, affiliate collaborations and LIVE shopping. These opportunities have separate approval and commercial terms.</p></article></div>
<h2>Building with local experience</h2><p>We are looking for people who understand their creators, language and market. Managers can share experience, availability and proposed rates through their country page.</p>
<p>Based in the US? <a href="{u('/apply/')}">See the US LIVE application</a>. Interested in another country? <a href="{e(wa())}" target="_blank" rel="noopener noreferrer">Tell us on WhatsApp</a>.</p>'''


def shop_body(u):
    return f'''<section class="hero"><span class="badge">Shop expressions of interest</span><h1>Products you understand.<br>Content people trust.</h1><p class="lede">Tell us about your niche, product content and experience with affiliate or LIVE shopping. We’re gathering interest for Sparked’s Shop development.</p><a class="btn" href="#interest">Discuss Shop opportunities</a></section>
<div class="note">This is an inquiry, not enrollment into an approved Sparked Shop agency. Shop participation, market eligibility and commercial terms must be confirmed separately. Our US LIVE network relationship does not establish Shop approval.</div>
<div class="grid"><article class="card"><h2>Creators</h2><p>Share the products you know, the audience you serve and the kind of support you want.</p></article><article class="card"><h2>Managers and brands</h2><p>Tell us about your market, creator experience and proposed collaboration.</p></article></div>
<p>Prefer a local introduction? <a href="{u('/uk/')}">UK</a> · <a href="{u('/brazil/')}">Brasil — Português</a> · <a href="{u('/mexico/')}">México — Español</a></p>
{interest_form(u, shop=True, message='Hi Sparked Live, I would like to discuss a Shop opportunity.')}'''
