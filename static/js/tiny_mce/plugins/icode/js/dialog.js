tinyMCEPopup.requireLangPack();

var icodeDialog = {
    init: function() {
        var f = document.forms[0];

        // Get the selected contents as text and place it in the input
        f.txtCode.value = tinyMCEPopup.editor.selection.getContent({format : 'text'});      
    },

    insert: function() {
        // Insert the contents from the input into the document
        tinyMCEPopup.editor.execCommand('mceInsertContent', false, GetFormatedCode());
        tinyMCEPopup.close();
    }
};

function GetFormatedCode() {
    var strCode = document.forms[0].txtCode.value;

    strCode = strCode.replace(/</gi,"&lt;");
    strCode = strCode.replace(/>/gi, "&gt;");
    var strCodeText = '<div id="CodeDiv" dir="ltr"><pre  class="brush: ' + document.forms[0].selctLanguage.value + '">';
    strCodeText += strCode;
    strCodeText += '</pre></div><br/>';
    return strCodeText;
}

tinyMCEPopup.onInit.add(icodeDialog.init, icodeDialog);
