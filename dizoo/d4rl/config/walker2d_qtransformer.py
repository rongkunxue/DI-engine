# You can conduct Experiments on D4RL with this config file through the following command:
# cd ../entry && python d4rl_qtransformer_main.py
from easydict import EasyDict
from ding.model import QTransformer


num_timesteps = (10,)

main_config = dict(
    exp_name="walker2d_qtransformer",
    # env=dict(
    #     env_id="hopper-medium-expert-v0",
    #     collector_env_num=5,
    #     evaluator_env_num=8,
    #     use_act_scale=True,
    #     n_evaluator_episode=8,
    #     stop_value=6000,
    # ),
    dataset=dict(
        dataset_folder="./dataset/model",
        num_timesteps=num_timesteps,
    ),
    policy=dict(
        cuda=True,
        model=dict(
            num_timesteps=num_timesteps,
            state_dim=11,
            action_dim=7,
            action_bin=256,
        ),
        learn=dict(
            data_path=None,
            train_epoch=3000,
            batch_size=2048,
            learning_rate_q=3e-4,
            alpha=0.2,
            discount_factor_gamma=0.99,
            min_reward=0.0,
            auto_alpha=False,
        ),
        collect=dict(
            data_type="d4rl",
        ),
        eval=dict(
            evaluator=dict(
                eval_freq=5,
            )
        ),
        other=dict(
            replay_buffer=dict(
                replay_buffer_size=2000000,
            ),
        ),
    ),
)

main_config = EasyDict(main_config)
main_config = main_config

create_config = dict(
    env=dict(
        type="mujoco",
        import_names=["dizoo.mujoco.envs.mujoco_env"],
    ),
    env_manager=dict(type="subprocess"),
    policy=dict(
        type="sac",
        import_names=["ding.policy.sac"],
    ),
    replay_buffer=dict(
        type="naive",
    ),
)
create_config = EasyDict(create_config)
create_config = create_config

if __name__ == "__main__":
    # or you can enter `ding -m serial -c walker2d_sac_config.py -s 0`
    from ding.entry import serial_pipeline_offline

    model = QTransformer(**main_config.policy.model)
    serial_pipeline_offline([main_config, create_config], seed=0, model=model)
