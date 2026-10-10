#import <Foundation/Foundation.h>

@protocol HureaDispatchProtocol
- (void)performAction:(id)sender;
@optional
- (int)optionalFixtureValue;
@end

@interface HureaDispatchFixture : NSObject <HureaDispatchProtocol> {
  int state;
}
- (void)performAction:(id)sender;
+ (int)fixtureVersion;
@end
@implementation HureaDispatchFixture
- (void)performAction:(id)sender { state += sender == nil ? 1 : 2; }
+ (int)fixtureVersion { return 1; }
@end
int main(void) { return 0; }
