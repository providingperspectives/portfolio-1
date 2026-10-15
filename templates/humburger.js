// Hamburger menu toggle
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.getElementById('nav-menu');

        if (hamburger) {
            hamburger.addEventListener('click', function() {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
            });
        }

        // Close menu when clicking on a link
        document.querySelectorAll('#nav-menu li a').forEach(link => {
            link.addEventListener('click', function() {
                if (hamburger) hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Lightbox / project preview
        function openLightbox(src, title, desc, endpoint){
            const lb = document.getElementById('lightbox');
            lb.querySelector('img').src = src;
            lb.querySelector('.info h3').textContent = title;
            lb.querySelector('.info p').textContent = desc;
            lb.querySelector('.view-link').href = '/portfolio/' + endpoint;
            lb.classList.add('open');
            lb.setAttribute('aria-hidden','false');
            lb.querySelector('.close').focus();
        }
        function closeLightbox(){
            const lb = document.getElementById('lightbox');
            lb.classList.remove('open');
            lb.setAttribute('aria-hidden','true');
        }

        document.addEventListener('click', function(e){
            const thumb = e.target.closest('.thumb-wrap');
            if(thumb){
                const img = thumb.querySelector('img');
                const src = img.src;
                const title = thumb.dataset.title || '';
                const desc = thumb.dataset.desc || '';
                const endpoint = thumb.dataset.endpoint || '';
                e.preventDefault();
                openLightbox(src, title, desc, endpoint);
            }

            if(e.target.matches('#lightbox') || e.target.closest('#lightbox .close')){
                closeLightbox();
            }
        });

        document.addEventListener('keydown', function(e){
            if(e.key === 'Escape') closeLightbox();
        });
