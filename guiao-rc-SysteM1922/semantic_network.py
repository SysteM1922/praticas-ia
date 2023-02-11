

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#

class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2)]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))


################# Exercícios Guião #################

    def list_associations(self):
        return {i.relation.name for i in self.query_local() if type(i.relation) is Association}

    def list_objects(self):
        return {i.relation.entity1 for i in self.query_local() if type(i.relation) is Member}

    def list_users(self):
        return {i.user for i in self.query_local()}

    def list_types(self):
        return {i.relation.entity1 and i.relation.entity2 for i in self.query_local() if type(i.relation) is Subtype}.union({i.relation.entity2 for i in self.query_local() if type(i.relation) is Member})
        
    def list_local_associations(self, entity):
        return {i.relation.name for i in self.query_local(e1=entity) if type(i.relation) is Association}

    def list_relations_by_user(self, user):
        return {i.relation.name for i in self.query_local(user=user)}

    def associations_by_user(self, user):
        return len({i.relation.name for i in self.query_local(user=user) if type(i.relation) is Association})

    def list_local_associations_by_entity(self, entity):
        return {(i.relation.name, i.user) for i in self.query_local(e1=entity) if type(i.relation) is Association}

    def predecessor(self, A, B):
        query = self.query_local(e2=A)
        if query == []:
            return False
        for i in query:
            if type(i.relation) in (Member, Subtype) and i.relation.entity1 == B:
                return True
        
        return self.predecessor(i.relation.entity1, B)

    def predecessor_path(self, A, B):
        query = self.query_local(e2=A)
        if query == []:
            return None
        for i in query:
            if type(i.relation) in (Member, Subtype) and i.relation.entity1 == B:
                return [A, B]
        
        return [A] + self.predecessor_path(i.relation.entity1, B)

    def query(self, entity, relation=None):
        ret = [i for i in self.query_local(e1=entity, rel=relation) if type(i.relation) is Association]
        for e in self.list_types():
            if self.predecessor(e, entity):
                ret.extend([i for i in self.query_local(e1=e, rel=relation) if type(i.relation) is Association])
        return ret

    def query2(self, entity, relation=None):
        ret = [i for i in self.query_local(e1=entity, rel=relation) if type(i.relation) in (Association, Member, Subtype)]
        for e in self.list_types():
            if self.predecessor(e, entity):
                ret.extend([i for i in self.query_local(e1=e, rel=relation) if type(i.relation) is Association])
        return ret

    def query_cancel(self, entity, relation=None):
        ret=[]
        for i in self.query_local(e1=entity):
            if type(i.relation) is Member:
                ret += self.query_local(e1=i.relation.entity2, rel=relation)
        return ret

    def query_down(self, tipo, relation=None):
        ret = []
        for i in self.query_local():
            if i.relation.entity2 == tipo and type(i.relation) is Subtype:
                ret += self.query_local(e1=i.relation.entity1, rel=relation) + self.query_down(i.relation.entity1, relation)
        return ret

    def query_induce(self, tipo, relation):
        ret=[]
        for i in self.query_down(tipo, relation):
            ret.append(i.relation.entity2)
        return max(set(ret), key=ret.count)

    def query_local_assoc(self, entity, relation):
        query = [i.relation for i in self.query_local(e1=entity, rel=relation)]
        try:
            tipo = type(query[0])
            query = [(i.name, i.entity2) for i in query]
        except:
            pass
        
        if tipo is Association:
            ret = []
            for i in range(len(set(query))):
                if sum(x[1] for x in ret) < 0.75:
                    val = sorted(set(query), key=lambda x:query.count(x), reverse=True)[i]
                    ret.append((val[1], query.count(val)/len(query)))
                else:              
                    return ret
        elif tipo is AssocOne:
            return max([(i[1], query.count(i)/len(query)) for i in set(query)], key=lambda x: x[1])
        elif tipo is AssocNum:
            return sum(i[1] for i in query)/len(query) 
        else:
            return None

    def query_assoc_value(self, entity, relation):
        def percentagem(lst, V):
            return len([i for i in lst if i[1]==V])/len(lst) if len(lst) != 0 else 0
        query = [(i.relation.entity1, i.relation.entity2) for i in self.query_local(rel=relation) if i.relation.entity1 != entity and self.predecessor(i.relation.entity1, entity)]
        query2 = [(i.relation.entity1, i.relation.entity2) for i in self.query_local(e1=entity, rel=relation)]
        if len(set(query2))==1:
            return query[0][1]
        elif len(query) == 0:
            return max(query2, key = lambda x:percentagem(query2, x[1]))[1]
        elif len(query2) == 0:
            return max(query, key = lambda x:percentagem(query, x[1]))[1]
        else:
            return max(query2, key = lambda x:(percentagem(query, x[1])+percentagem(query2, x[1]))/2)[1]
            
        
                
            