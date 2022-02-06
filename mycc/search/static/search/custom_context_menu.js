    $(function() {
        $.contextMenu({
            selector: '.context-menu-one',
            callback: function(key, options) {
                var m = "clicked: " + key;
                window.console && console.log(m) || alert(m);
            },
            items: {
                "folder": {name: "Open Folder in New Tab"},
            }
        });

        $('.context-menu-one').on('click', function(e){
            console.log('clicked', this);
        })
    });