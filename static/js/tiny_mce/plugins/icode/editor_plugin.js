/**
 * $Id: editor_plugin_src.js 201 2007-02-12 15:56:56Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2008, Moxiecode Systems AB, All rights reserved.
 */

(function() {
	// Load plugin specific language pack
tinymce.PluginManager.requireLangPack('icode');

tinymce.create('tinymce.plugins.icodePlugin', {
		/**
		 * Initializes the plugin, this will be executed after the plugin has been created.
		 * This call is done before the editor instance has finished it's initialization so use the onInit event
		 * of the editor instance to intercept that event.
		 *
		 * @param {tinymce.Editor} ed Editor instance that the plugin is initialized in.
		 * @param {string} url Absolute URL to where the plugin is located.
		 */
		init : function(ed, url) {
			// Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceicode');
			ed.addCommand('mceicode', function() {
				ed.windowManager.open({
					file : url + '/dialog.htm',
					width: 700 + parseInt(ed.getLang('icode.delta_width', 0), 10),
					height: 300 + parseInt(ed.getLang('icode.delta_height', 0), 10),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			// Register icode button
			ed.addButton('icode', {
			    title: 'Syntax Highlighting for Code',
				cmd : 'mceicode',
				image : url + '/img/icode.png'
			});

		    ed.onNodeChange.add(this._nodeChange, this);
			ed.onVisualAid.add(this._visualAid, this);
		},
        _nodeChange: function(ed, cm, n) {
			var p = ed.dom.getParent(n, 'DIV.mce_icode_container');
            if (p == null)
                p = ed.dom.getParent(n, 'DIV.codehilite');
			if (p) {
				cm.setActive('icode', 1);
				ed.selection.select(p);
			} else {
			    cm.setActive('icode', 0);
			}
        },
        _visualAid : function(ed, e, s) {
            var dom = ed.dom;

			tinymce.each(dom.select('DIV.mce_icode_container', e), function(e) {
				if (s)
					dom.addClass(e, 'mceItemVisualAid');
				else
					dom.removeClass(e, 'mceItemVisualAid');	
			});
		},
		getInfo : function() {
			return {
				longname : 'icode plugin',
				author : 'Some author',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/example',
				version : "1.0"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('icode', tinymce.plugins.icodePlugin);
})();