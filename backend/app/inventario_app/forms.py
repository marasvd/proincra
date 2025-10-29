from django import forms
from .models import EntradaInventario, SalidaInventario, Producto

class FiltroProductoForm(forms.Form):
    q = forms.CharField(label="Buscar", required=False)
    estado = forms.ChoiceField(
        required=False,
        choices=(('', 'Todos'), ('ok', 'Disponible'), ('low', 'Bajo stock')),
    )
    tipo = forms.ChoiceField(
        required=False,
        choices=(('', 'Todos'), ('herramienta', 'Herramienta'), ('material', 'Material')),
    )

class EntradaForm(forms.ModelForm):
    class Meta:
        model = EntradaInventario
        fields = ['producto', 'cantidad', 'proveedor', 'observaciones']

class SalidaForm(forms.ModelForm):
    class Meta:
        model = SalidaInventario
        fields = ['producto', 'cantidad', 'destino', 'observaciones']
