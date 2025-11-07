from django import forms
from .models import EntradaInventario, SalidaInventario
from app.productos_app.models import Producto
from app.proveedores_app.models import Proveedor

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
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        label="Producto",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        label="Proveedor",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = EntradaInventario
        fields = ['producto', 'proveedor', 'cantidad', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre} - {obj.categoria}"

        # Asignar clases Bootstrap
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})
        self.fields['proveedor'].widget.attrs.update({'class': 'form-select'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['observaciones'].widget.attrs.update({'class': 'form-control'})

class SalidaForm(forms.ModelForm):
    class Meta:
        model = SalidaInventario
        fields = ['producto', 'cantidad', 'destino', 'observaciones']
