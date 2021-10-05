from pprint import pprint
import re
import yaml

class Topology:
    def __init__(self,topology_dict):
        self.topology = self._normalize(topology_dict)
        self.element = list(self.topology.items())
    def _normalize(self,topology_dict):
        reversed_dict  = {v:k for k,v in topology_dict.items()}
        dup_list = []
        uniq_list = []
        for entry in topology_dict.items():
            if entry in dup_list:
                continue
            for entry_2 in reversed_dict.items():
                if entry == entry_2:
                    a,b = entry
                    add_to_list = (b,a)
                    dup_list.append(add_to_list)
            uniq_list.append(entry)
        return dict(uniq_list)
    def delete_link(self,*link):
        a,b = link
        reversed_link = (b,a)
        list_without_link = []
        copy_dict = self.topology.copy()
        for item in self.topology.items():
            if item == link or item == reversed_link:
                continue
            list_without_link.append(item)
        if list_without_link != list(self.topology.items()):
            self.topology = dict(list_without_link)
        else:
            print(f"link {link} is not in topology")
    def delete_node(self,device):
        updated_list = []
        for link in self.topology.items():
            if device in link[0] or device in link[1]:
                continue
            else:
                updated_list.append(link)
        if len(self.topology) == len(dict(updated_list)):
            print (f'There is no such device as "{device}"')
        else:
            self.topology = dict(updated_list)
    def add_link (self,a,b):
        link = (a,b)
        reversed_link = (b,a)
        all_element = set(list(self.topology.keys()) + list(self.topology.values()))
        type1 = list(self.topology.items())
        if any(link == x for x in type1) or any(reversed_link == y for y in type1):
            print ('Such a Connection already exist')
        elif a in all_element or b in all_element:
            print("connection to one of the node exist")
        else:
            self.topology.update({a:b})
    def __getitem__(self, index):
        return self.element[index]
    def __iter__(self):
        return iter(self.element)
    def __len__(self):
        return len(self.element)
    def __add__(self,other):
        topology_copy = self.topology.copy()
        return Topology(topology_copy.update(other.topology))

if __name__ == "__main__":
    topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                        ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                        ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                        ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                        ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                        ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                        ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                        ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                        ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}
    #topo = Topology(topology_example)
    #pprint(topo.topology)
    #print ('\n')
    #topo.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
    #pprint(topo.topology)
    #print('\n')
    #topo.delete_node('R1')
    #pprint(topo.topology)
    t1 = Topology({('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R3', 'Eth0/6'): ('R10', 'Eth0/0')})
    topology_example2 = {('R2', 'Eth0/4'): ('R7', 'Eth0/0'),('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
    t2 = Topology(topology_example2)
    t3 = t1 + t2
    print (t3.topology)



