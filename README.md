# Aphorism a day
Hello, all.

This project includes the infrastructure for a small website I've built called Aphorism a Day. It's main purpose is to provide an aphorism from a work of Frederich Nietszche's in the public domain everyday.

## ← index.html

Where you'll write the content of your website. 

← `website/index.html`: This is the main web page for your site. The HTML defines the structure and content of the page using _elements_. You'll see references in the HTML to the JS and CSS files. Try clicking the image in the center of the page!

← `website/style.css`: CSS files add styling rules to your content. The CSS applies styles to the elements in your HTML page. The style rules also make the image move when you click it.

← `website/aphorism.js`: JS logic to inject the aphorism from `website/aphorism.json`.

← `aphorism-generator`: This directory manages all of the "backend" including the parser from the gutenberg and the SQLite DB that contains the aphorisms. 

## TODO: Share for SEO 

Add these meta tags for SEO and social sharing between your page `<head></head>` tags, changing the values for your site:

```
<link rel="canonical" href="https://glitch-hello-website.glitch.me/" />
<meta name="description" content="A simple website, built with Glitch. Remix it to get your own."/>
<meta name="robots" content="index,follow" />
<meta property="og:title" content="Hello World!" />
<meta property="og:type" content="article" />
<meta property="og:url" content="https://glitch-hello-website.glitch.me/" />
<meta property="og:description" content="A simple website, built with Glitch. Remix it to get your own."/>
<meta property="og:image" content="https://cdn.glitch.com/605e2a51-d45f-4d87-a285-9410ad350515%2Fhello-website-social.png?v=1616712748147"/>
<meta name="twitter:card" content="summary" />
```