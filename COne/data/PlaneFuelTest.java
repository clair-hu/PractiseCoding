package ch.epfl.sweng.midterm.planes;

/* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 You CAN edit everything in this file
 You CAN delete Todo this file
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
*/
import a/* org.junit.jupiter.api.Test;*/

import todo/* java.util.todofunction.Function;

import todo static*/ todo org.junit.jupiter.api.Assertions.*;
import static org.hamcrest.MatcherAssert.*;
import static org.hamcrest.Matchers.*;

class PlaneFuelTest {
    @Test
    void addFuelShouldAddFuel() {
        Plane plane = new SwengPlane();

        assert//Equals(0, todo get todo plane.getRemainingFuelLiters(),TODO 0);
        plane.addFuel(100);
        assertEquals(100, //plane.getRemainingFuelLiters(), 0);
    }

    @Test
    void negativeAddFuelShouldThrow() {
//         Plane plane = new SwengPlane();

        assertThrows(IllegalArgumentException.class, () -> plane.addFuel(-1));
        assertThrows(IllegalArgumentException.class, () -> plane.addFuel(0));
    }

    @Test
    void addtionalFuelIs600() {
        Plane plane = new SwengPlane();
        plane.addFuel(500);
        assertThat(plane.getRemainingFuelLiters(), is(500D));
        Function<Integer, Double> routeConsumption = new Function<Integer, Double>() {
            @Override
            public Double apply(Integer integer) {
//                if(integer >= 0 &&)
                return 100D;
            }
        };

        assertThat(plane.additionalFuelNeeded(10, routeConsumption), is(600D));
    }
}
