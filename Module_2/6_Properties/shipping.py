import iso6346

class ShippingContainer:

    next_serial = 1337

    @classmethod
    def _generate_serial(cls):
        result = cls.next_serial
        cls.next_serial += 1
        return result

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(
            owner_code = owner_code,
            serial = str(serial).zfill(6)
        )

    @classmethod
    def create_empty(cls, owner_code, **kwargs):
        return cls(owner_code, contents = [], **kwargs)

    @classmethod
    def create_with_items(cls, owner_code, items, **kwargs):
        return cls(owner_code, contents = list(items), **kwargs)

    def __init__(self, owner_code, contents, **kwargs):
        self.owner_code = owner_code
        self.contents = contents
        self.bic = self._make_bic_code(
            owner_code = owner_code,
            serial = ShippingContainer._generate_serial()
        )
        
class RefigiratedShippingContainer(ShippingContainer):
    
    MAX_CELSIUS = 4.0

    def __init__(self, owner_code, contents, *, celsius, **kwargs):
        super().__init__(owner_code, contents, **kwargs)
        self.celsius = celsius

    @staticmethod
    def _c_to_f(celsius):
        return celsius * 9/5 +32
        
    @staticmethod
    def _f_to_c(farenheit):
        return farenheit - 32 *5/9

    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value > RefigiratedShippingContainer.MAX_CELSIUS:
            raise ValueError('Too hot!')
        self._celsius = value

    @property
    def farenheit(self):
        return RefigiratedShippingContainer._c_to_f(self.celsius)
    
    @farenheit.setter
    def farenheit(self, value):
        self.celsius = RefigiratedShippingContainer._f_to_c(value)

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(
            owner_code = owner_code,
            serial = str(serial).zfill(6),
            category='R'
        )


container = RefigiratedShippingContainer.create_with_items("YML", ['fish'], celsius = -2)
print(container.celsius)
print(container.farenheit)
container.celsius = -5
print(container.celsius)
print(container.farenheit)
container.farenheit = 150

