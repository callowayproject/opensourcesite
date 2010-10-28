tinyMCEPopup.requireLangPack();

var icodeDialog = {
    isNew: true,
    
    container: {},
    
    init: function() {
        var f = document.forms[0];
        var ed = tinyMCEPopup.editor;
		this.container = this.getICodeContainer(ed.selection.getStart());
		this.isNew = (this.container === null);
        
        if (this.isNew)
            f.txtCode.value = ed.selection.getContent({format : 'text'});
        else if (this.container.firstElementChild.tagName == 'PRE')
            f.txtCode.value = this.container.firstElementChild.innerText || '';
        else if (this.container.tagName == 'PRE'){
            f.txtCode.value = this.container.innerText || '';
        }
    },
    getICodeContainer: function(el) {
		var ed = tinyMCEPopup.editor;
        var p = ed.dom.getParent(el, 'DIV.mce_icode_container');
        if (p === null )
            p = ed.dom.getParent(el, 'DIV.codehilite');
        if (p === null)
            p = ed.dom.getParent(el, 'PRE');
        return p;
	},
    createICodeContainer: function(brush, text){
        var ed = tinyMCEPopup.editor;
		var cont_args = {'class': 'mce_icode_container'};
		var pre_args = {'class': 'brush: ' + brush};
		var container = ed.dom.create('div', cont_args);
		ed.dom.add(container, ed.dom.create('pre', pre_args, text));
		return container;
    },
    getFormattedCode: function() {
        var strCode = document.forms[0].txtCode.value;
        
        strCode = strCode.replace(/</gi,"&lt;");
        strCode = strCode.replace(/>/gi, "&gt;");
        return strCode;
    },
    insert: function() {
        var ed = tinyMCEPopup.editor;
        var brush = document.forms[0].selctLanguage.value;
        
        var container = this.createICodeContainer(brush, this.getFormattedCode());
        
        if (this.isNew) {
            try {
                var cur_sel = ed.selection.getNode();
                if (cur_sel === null)
                    ed.selection.setNode(container);
                else
                    ed.dom.insertAfter(container, cur_sel);
                ed.undoManager.add();
            } catch(e) {
                console.log(e);
                alert(e);
            }
        } else {
            ed.selection.select(this.container);
            ed.selection.setNode(container);
        }
        tinyMCEPopup.close();
    }
};


tinyMCEPopup.onInit.add(icodeDialog.init, icodeDialog);
