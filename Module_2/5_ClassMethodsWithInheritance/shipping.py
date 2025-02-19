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

    # without kwargs 'keyword args', the celsius parameter cannot be passed on 
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
        if celsius > RefigiratedShippingContainer.MAX_CELSIUS:
            raise ValueError('Too hot!')
        self.celsius = celsius

    @staticmethod
    def _make_bic_code(owner_code, serial):
        return iso6346.create(
            owner_code = owner_code,
            serial = str(serial).zfill(6),
            category='R'
        )


container = RefigiratedShippingContainer.create_with_items("YML", ['fish'], celsius = 2)
print(container.bic)
print(container.celsius)

