from flask import current_app

SWATCH_KEY = "ADMIN_SWATCH"


class ThemeChanger(object):
    def set_swatch(self, swatch):
        # update returns empty list when not exists
        #data = {"name": SWATCH_KEY, "rawvalue": swatch}
        #self.values.update(data, name=SWATCH_KEY) or self.values.create(**data)

        self.swatch = swatch
        self.save()


    @property
    def swatch(self):
        return self.swatch or 'default'
        #return self.get_value(SWATCH_KEY,
        #                      current_app.config.get(SWATCH_KEY, 'default'))
