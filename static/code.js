jQuery(
    function () {
	jQuery('a.dir').click(
	    function(e) {
		e.preventDefault();
		window.location = $(this).attr('href');
		return false;
	    }
	);

	jQuery('a.ajax').click(
	    function(e) {
		e.preventDefault();
		var $this = jQuery(this);
		var href = $this.attr('href');
		var content = {'cmd' : $this.attr('data-cmd')};
		jQuery.post(href, content,
			    function(e) {
				if(e.redirect != false) {
				    window.location = e.redirect;
				}
			    }, 'json');
		return false;
	    }
	);
});
