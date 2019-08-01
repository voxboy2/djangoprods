import redis
from django.conf import settings
from .models import Item


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_item_key(self, ed):
        return 'item:{}:purchased_with'.format(ed)

    def items_bought(self, items):
        item_eds = [p.ed for p in items]
        for item_ed in item_eds:
            for with_ed in item_eds:
                # get the other products bought with each product
                if item_ed != with_ed:
                    # increment score for product purchased together
                    r.zincrby(self.get_item_key(item_ed),
                              with_ed,
                              amount=1)

    def suggest_items_for(self, items, max_results=6):
        item_eds = [p.ed for p in items]
        if len(items) == 1:
            # only 1 product
            suggestions = r.zrange(
                             self.get_item_key(item_ids[0]),
                             0, -1, desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_eds = ''.join([str(ed) for ed in item_eds])
            tmp_key = 'tmp_{}'.format(flat_eds)
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_item_key(ed) for ed in item_eds]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *item_eds)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, 
                                   desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_items_eds = [int(ed) for ed in suggestions]

        # get suggested products and sort by order of appearance
        suggested_items = list(Item.objects.filter(ed__in=suggested_items_eds))
        suggested_items.sort(key=lambda x: suggested_items_eds.index(x.ed))
        return suggested_items

    def clear_purchases(self):
            for ed in Item.objects.values_list('ed', flat=True):
                r.delete(self.get_item_key(ed))