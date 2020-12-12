from ui.generators.CreateMenuPopup import CreateMenuPopup


class CreateMenuEffectEdit(CreateMenuPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setSelection(self, selection, selection_store, button=None):
        selection_store = selection
        # Change text of button if button features text
        if button:
            button.setText(selection)
