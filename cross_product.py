import random


class RandomCrossProduct:
    """
    Efficient way to iterate over a shuffled cross product of two sets without
    having to pre-compute the cross product.
    """

    def __init__(self, set1, set2):
        self._set1 = set1
        self._set2 = set2

    def __iter__(self):
        buckets = {x: None for x in self._set1}
        total_count = len(self._set1) * len(self._set2)
        while total_count > 0:
            i = random.randrange(total_count)
            for bucket, bucket_items in buckets.copy().items():
                i -= len(self._set2) if bucket_items is None else len(bucket_items)
                if i >= 0:
                    continue
                if bucket_items is None:
                    bucket_items = list(self._set2)
                    buckets[bucket] = bucket_items
                idx = random.randrange(len(bucket_items))
                obj = bucket_items[idx]
                del bucket_items[idx]
                yield bucket + obj
                break
            total_count -= 1

    def __len__(self):
        return len(self._set1) * len(self._set2)
