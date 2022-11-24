from xformer.tools.register import XFormerRegister, XFormerModuleType


def build_trainer(
        config: dict = None, default_args: dict = None,
        module_type: str = 'trainer', class_name: str = None,
        *args, **kwargs):
    if config is None and class_name is None:
        return None
    if config is not None:
        return XFormerRegister.get_instance_from_cfg(
            config, XFormerModuleType.TRAINER, default_args=default_args)
    return XFormerRegister.get_instance(module_type, class_name, *args, **kwargs)