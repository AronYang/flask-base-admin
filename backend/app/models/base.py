# coding=utf-8
import datetime

from flask import abort
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SessionMixin(object):

    def to_dict(self):
        '''用来序列化Model对象的函数
        '''
        value = {}
        for column in self.__table__.columns:
            attribute = getattr(self, column.name)
            if isinstance(attribute, datetime.datetime):
                attribute = str(attribute)
            value[column.name] = attribute
        return value

    @classmethod
    def add(cls, data):
        ''' 添加数据
        '''
        a = cls(**data)
        db.session.add(a)
        db.session.commit()
        db.session.refresh(a)
        return a

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """
        delete model
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def update(cls, _id, data):
        item = cls.query.get(_id)
        if not item:
            abort(404)
        for k, v in data.items():
            setattr(d, k, v)
        item.save()
        return item

    @classmethod
    def get_all(cls, query=None, get_query=False, operator="==", **params):
        """
        :param query: chain multiple get_all calls
        :param get_query: return the query object or all()
        :param operator: filter operators
        :param params: query parameter
        :return: object or list
        """
        query = query or cls.query
        for key, value in params.items():
            if not hasattr(cls, key):
                continue
            if operator == '==':
                query = query.filter(getattr(cls, key) == value)
            elif operator == '!=':
                query = query.filter(getattr(cls, key) != value)
            elif operator == 'LIKE':
                query = query.filter(getattr(cls, key).like(value))
            elif operator == 'ILIKE':
                query = query.filter(getattr(cls, key).ilike(value))
            elif operator == 'IN':
                query = query.filter(getattr(cls, key).in_(value))
            elif operator == 'NOT_IN':
                query = query.filter(~getattr(cls, key).in_(value))
            elif operator == 'IS_NULL':
                query = query.filter(getattr(cls, key).is_(None))
            elif operator == 'IS_NOT_NULL:':
                query = query.filter(getattr(cls, key).isnot(None))
            elif operator == 'MATCH':
                raise LookupError("support for match is not clear")
            else:
                raise LookupError("invalid operator")

        if get_query:
            return query
        return query.all()

    @classmethod
    def paginate(cls, query=None, page=None, per_page=None, error_out=False, max_per_page=None):
        """
        :param page: the number of pages of the query
        :param per_page: per page data item
        :param error_out: when error_out is True(default), the following rules will cause a 404 response:
        :param max_per_page: maximum data per page
        :return: dict | {"page": ${page}, "per_page": ${per_page}, "items": ${items}, "pages": ${pages}}
        """

        if request:
            if not page:
                try:
                    page = int(request.args.get('page', 1))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)
                    page = 1

            if not per_page:
                try:
                    per_page = int(request.args.get('per_page', 20))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)
                    per_page = 20

        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                abort(404)
            else:
                page = 1

        if per_page < 0:
            if error_out:
                abort(404)
            else:
                per_page = 20
        query = query or cls.query
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.count()

        if per_page == 0:
            total_page = 0
        else:
            total_page = int(ceil(total / float(per_page)))

        items = [
            (
                marshal if callable(marshal) else None
                or
                (lambda obj: (getattr(obj, "marshal") if hasattr(obj, "marshal") else None or obj.to_dict)())
            )(item)
            for item in items
        ]

        return {"current_page": page, "per_page": per_page, "items": items, "total_page": total_page}
