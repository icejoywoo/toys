#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/swap-nodes-in-pairs/
    @author: icejoywoo
    @date: 2019-09-28
"""


# helper function to convert python list to ListNode
def list_node(l):
    if l:
        nodes = [ListNode(i) for i in l]
        head = nodes[0]
        p = head
        for i in nodes[1:]:
            p.next = i
            p = i
        return head
    else:
        return None


# Definition for singly-linked list.
class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None

    def _to_list(self):
        p = self
        r = []
        while p:
            r.append(p.val)
            p = p.next
        return r

    def __repr__(self):
        return 'ListNode{val: %r, next: %r}' % (self.val, self.next._to_list() if self.next else None)


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def swapPairs1(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None:
            return None

        p, c, q = None, head, head.next
        # when len == 1, q is None
        r = q if q else c
        # 奇数节点与偶数节点情况略有不同
        while q:
            c.next, q.next = q.next, c

            if p:
                p.next = q

            # update p, c, q
            p, c = c, c.next
            q = c.next if c else None

        return r

    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        dummy = ListNode(None)
        prev, prev.next = dummy, head
        while prev.next and prev.next.next:
            a = prev.next
            b = prev.next.next
            a.next, b.next = b.next, a
            prev.next = b
            prev = a
        return dummy.next


if __name__ == '__main__':
    s = Solution()
    print s.swapPairs(list_node([]))
    print s.swapPairs(list_node([1]))
    print s.swapPairs(list_node([1, 2, 3, 4, 5]))  # 2 1 4 3 5
    print s.swapPairs(list_node([1, 2, 3, 4]))  # 2 1 4 3
