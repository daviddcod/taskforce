from django import template
from wdmmorpg.models import PriorityScale, Rank

register = template.Library()

@register.filter(name='priority_filter')
def priority_filter(items, rank):
    # Filter items based on whether their priority's rank matches the given rank
    filtered_items = [item for item in items if item.priority.rank == rank]
    return filtered_items
