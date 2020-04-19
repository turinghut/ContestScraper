import process from 'process';

const init = (closeFunc: () => void) => async (): Promise<void> => {
  try {
    await closeFunc();
    process.exit(0);
  } catch (err) {
    process.exit(1);
  }
};

// For now we are exporting init by default. In future, we might need more commands
export default init;
