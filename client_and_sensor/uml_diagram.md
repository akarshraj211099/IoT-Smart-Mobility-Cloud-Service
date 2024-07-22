classDiagram
    class User {
        - username: CharField
        - password: CharField
    }

    class GroupAdmin {
        - user: OneToOneField(User)
        - group_name: CharField
    }

    class Group {
        - name: CharField
        - max_students: IntegerField
    }

    class UserProfile {
        - user: OneToOneField(User)
        - group: ForeignKey(Group)
    }

    class Student {
        - user: OneToOneField(User)
        - group_admin: ForeignKey(GroupAdmin)
    }

    UserProfile --> User : 1 to 1
    Student --> User : 1 to 1
    GroupAdmin --> User : 1 to 1
    UserProfile --> Group : n to 1
    Student --> GroupAdmin : n to 1
    GroupAdmin --> Group : 1 to n
    Group --> UserProfile : 1 to n