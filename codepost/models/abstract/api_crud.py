# =============================================================================
# codePost v2.0 SDK
#
# CRUD ABSTRACT API RESOURCE VERBS SUB-MODULE
# =============================================================================

from __future__ import print_function # Python 2

# Python stdlib imports
import copy as _copy
import functools as _functools
import textwrap as _textwrap

# External dependencies
import better_exceptions as _better_exceptions

# Local imports
import codepost.util.logging as _logging
import codepost.api_requestor as _api_requestor

from . import api_resource as _api_resource

# =============================================================================

# Global submodule constants
_LOG_SCOPE = "{}".format(__name__)

# Global submodule protected attributes
_logger = _logging.get_logger(name=_LOG_SCOPE)

# =============================================================================

class CreatableAPIResource(_api_resource.AbstractAPIResource):
    
    def create(self, **kwargs):
        _class_type = type(self)
        
        # FIXME: do kwargs validation
        data = dict(getattr(self, "_data", dict()))
        data.update(_copy.deepcopy(kwargs))
        
        ret = self._requestor._request(
            endpoint=self.class_endpoint,
            method="POST",
            data=data,
        )
        if ret.status_code == 201:
            return _class_type(**ret.json)
    
    def saveInstanceAsNew(self, **kwargs):
        obj = self.create(**kwargs)

        # Sanity check
        assert (
            getattr(self, "_OBJECT_NAME", "") == 
            getattr(obj, "_OBJECT_NAME", ""))

        self._data = obj._data

        return self

        


# =============================================================================

class ReadableAPIResource(_api_resource.AbstractAPIResource):
    
    def retrieve(self, id, **kwargs):
        _class_type = type(self)
        ret = self._requestor._request(
            endpoint=self.instance_endpoint_by_id(id=id),
            method="GET",
            **kwargs
        )
        if ret.status_code == 200:
            return _class_type(**ret.json)
    
    def refreshInstance(self, id=None, **kwargs):
        # Figure out what ID to use
        id = self._get_id(id=id)
        if id == None:
            return
        
        obj = self.retrieve(id=id, **kwargs)

        # Sanity check
        assert (
            getattr(self, "_OBJECT_NAME", "") == 
            getattr(obj, "_OBJECT_NAME", ""))

        self._data = obj._data

        return self



# =============================================================================

class UpdatableAPIResource(_api_resource.AbstractAPIResource):
    
    def update(self, id, **kwargs):
        _class_type = type(self)
        ret = self._requestor._request(
            endpoint=self.instance_endpoint_by_id(id=id),
            method="PATCH",
            **kwargs
        )
        if ret.status_code == 200:
            return _class_type(**ret.json)
    
    def saveInstance(self, id=None, **kwargs):
        # Figure out what ID to use
        id = self._get_id(id=id)
        if id == None:
            return
        
        obj = self.update(id=id, **kwargs)

        # Sanity check
        assert (
            getattr(self, "_OBJECT_NAME", "") == 
            getattr(obj, "_OBJECT_NAME", ""))

        self._data = obj._data

        return self

# =============================================================================

class DeletableAPIResource(_api_resource.AbstractAPIResource):
    
    def delete(self, id, **kwargs):
        ret = self._requestor._request(
            endpoint=self.instance_endpoint_by_id(id=id),
            method="DELETE",
            **kwargs
        )
        return (ret.status_code == 204)
    
    def deleteInstance(self, id=None, **kwargs):
        # Figure out what ID to use
        id = self._get_id(id=id)
        if id == None:
            return
        
        return self.delete(id=id, **kwargs)

# =============================================================================



