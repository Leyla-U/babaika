console.log(Array.from(document.body.children).map(c => [c.id || c.className, c.offsetTop]));
console.log(Array.from(document.getElementById('mag-zoom-inner').children).map(c => [c.id || c.className, c.offsetTop]));
