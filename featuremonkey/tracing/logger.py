# coding: utf-8
from __future__ import unicode_literals

import abc
import copy
from typing import Any, Dict, Optional

OPERATION_LOG = list()


class OperationLogger(object):
    """
    Inherit from this interface to provide all required functionality for logging.
    Below there are two default classes which can be used for logging.
    """
    __metaclass__ = abc.ABCMeta
    operation_log = NotImplementedError("Please define the operation_log-Variable!")

    @abc.abstractmethod
    def log(self, operation: Optional[Dict[str, str]] = None, new_value: Any = "", old_value: Any = "") -> None:
        raise NotImplementedError("Please define the log-Method!")

    @abc.abstractmethod
    def log_old_value(self, operation: Optional[Dict[str, str]] = None, old_value: Any = "") -> None:
        raise NotImplementedError("Please define the log_old_value-Method!")

    @abc.abstractmethod
    def log_new_value(self, operation: Optional[Dict[str, str]] = None, new_value: Any = "") -> None:
        raise NotImplementedError("Please define the log_new_value-Method!")


class NullOperationLogger(OperationLogger):
    """
    Base class for logging the composer operations. Implement this and set it
    in your environment as COMPOSITION_TRACER for real tracing.
    To make the log accessible, use the OPERATION_LOG as your classes log attribute:
        self.operation_log = OPERATION_LOG
    """
    operation_log = OPERATION_LOG

    def log(self, operation: Optional[Dict[str, str]] = None, new_value: Any = "", old_value: Any = "") -> None:
        pass

    def log_old_value(self, operation: Optional[Dict[str, str]] = None, old_value: Any = "") -> None:
        pass

    def log_new_value(self, operation: Optional[Dict[str, str]] = None, new_value: Any = "") -> None:
        """
        Needed in case the old value must be logged before the new value is applied.
        This way both entries can be logged separately with their current values.
        :param operation:
        :param new_value:
        :return:
        """
        pass


class DefaultOperationLogger(OperationLogger):
    operation_log = OPERATION_LOG

    @staticmethod
    def _get_lazy_translation_value(value) -> str:
        """
        Special handling for top level (not nested in other data structures) lazy translation objects.
        This should prevent the translation process and so there is no import guard error.
        It should cover most cases of translation usage.
        :param value:
        :return:
        """
        if hasattr(value, '_proxy____args'):
            translation_args = getattr(value, '_proxy____args')
            return "".join(translation_args)

    def log(self, operation: Optional[Dict[str, str]] = None, new_value: str = "", old_value: Any = "") -> None:
        if operation is None:
            operation = dict()
        operation['new_value'] = copy.deepcopy(new_value)
        operation['old_value'] = copy.deepcopy(old_value)
        self.operation_log.append(operation)

    def log_new_value(self, operation: Optional[Dict[str, str]] = None, new_value: Any = "") -> None:
        if operation is None:
            operation = dict()
        translation_value = self._get_lazy_translation_value(new_value)
        if translation_value:
            self.operation_log[self.operation_log.index(operation)]['new_value'] = translation_value
        else:
            self.operation_log[self.operation_log.index(operation)]['new_value'] = copy.deepcopy(new_value)

    def log_old_value(self, operation: Optional[Dict[str, str]] = None, old_value: Any = "") -> None:
        pass
